"""
FastAPI Backend for PE Fund NAV Calculator
RESTful API for fund administration operations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
import tempfile

from nav_engine.nav_calculator import NAVCalculator
from nav_engine.fee_calculator import FeeCalculator
from nav_engine.reconciliation import ReconciliationEngine
from excel_integration.upload_valuations import ValuationUploader
from reporting.investor_statement import InvestorStatementGenerator

from config import API_CONFIG


# =====================================================
# Initialize FastAPI
# =====================================================

app = FastAPI(
    title=API_CONFIG['title'],
    description=API_CONFIG['description'],
    version=API_CONFIG['version']
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Pydantic Models
# =====================================================

class NAVRequest(BaseModel):
    fund_id: int = Field(..., description="Fund ID")
    calculation_date: date = Field(default_factory=date.today, description="Calculation date")


class NAVResponse(BaseModel):
    fund_id: int
    calculation_date: str
    nav: float
    gav: float
    total_liabilities: float
    tvpi: float
    dpi: float
    rvpi: float
    currency: str


class FeeRequest(BaseModel):
    fund_id: int
    calculation_date: date = Field(default_factory=date.today)


class FeeResponse(BaseModel):
    fund_id: int
    management_fee: float
    performance_fee: float
    total_fees: float
    currency: str
    waterfall_details: dict


class ReconciliationRequest(BaseModel):
    fund_id: int
    calculation_date: date = Field(default_factory=date.today)


class StatementRequest(BaseModel):
    fund_id: int
    investor_id: int
    as_of_date: date = Field(default_factory=date.today)


# =====================================================
# API Endpoints
# =====================================================

@app.get("/")
def root():
    """API health check"""
    return {
        "status": "healthy",
        "api": "PE Fund NAV Calculator",
        "version": API_CONFIG['version']
    }


@app.post("/calculate-nav", response_model=NAVResponse)
def calculate_nav(request: NAVRequest):
    """
    Calculate NAV for a fund
    
    Returns comprehensive NAV breakdown with performance metrics
    """
    try:
        calculator = NAVCalculator()
        
        result = calculator.calculate_nav(
            fund_id=request.fund_id,
            calculation_date=request.calculation_date,
            save_to_db=True
        )
        
        return {
            "fund_id": result['fund_id'],
            "calculation_date": str(result['calculation_date']),
            "nav": result['net_asset_value'],
            "gav": result['gross_asset_value'],
            "total_liabilities": result['total_liabilities'],
            "tvpi": result['tvpi'],
            "dpi": result['dpi'],
            "rvpi": result['rvpi'],
            "currency": result['nav_currency']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/calculate-fees", response_model=FeeResponse)
def calculate_fees(request: FeeRequest):
    """
    Calculate management and performance fees with waterfall breakdown
    """
    try:
        fee_calculator = FeeCalculator()
        
        result = fee_calculator.calculate_all_fees(
            fund_id=request.fund_id,
            calculation_date=request.calculation_date,
            save_to_db=True
        )
        
        return {
            "fund_id": result['fund_id'],
            "management_fee": result['management_fee']['period_fee'],
            "performance_fee": result['performance_fee']['performance_fee'],
            "total_fees": result['total_fees'],
            "currency": result['currency'],
            "waterfall_details": result['performance_fee']['waterfall']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reconcile")
def reconcile_nav(request: ReconciliationRequest):
    """
    Run comprehensive reconciliation checks on NAV
    
    Returns validation results for 5 key checks
    """
    try:
        engine = ReconciliationEngine()
        
        result = engine.run_full_reconciliation(
            fund_id=request.fund_id,
            calculation_date=request.calculation_date,
            save_to_db=True
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-valuations")
async def upload_valuations(
    file: UploadFile = File(...),
    fund_id: Optional[int] = None
):
    """
    Upload investment valuations from Excel file
    
    Expected format:
    | Investment Name | Valuation Date | Fair Value | Currency | Method | Source | Notes |
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Upload valuations
        uploader = ValuationUploader()
        result = uploader.upload_from_excel(tmp_path, fund_id)
        
        # Clean up
        os.unlink(tmp_path)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-statement")
def generate_investor_statement(request: StatementRequest):
    """
    Generate quarterly investor statement in Excel
    
    Returns file path to generated statement
    """
    try:
        generator = InvestorStatementGenerator()
        
        output_file = f"/home/claude/pe-fund-nav-calculator/reports/statement_fund{request.fund_id}_inv{request.investor_id}_{request.as_of_date}.xlsx"
        
        generator.generate_statement(
            fund_id=request.fund_id,
            investor_id=request.investor_id,
            as_of_date=request.as_of_date,
            output_file=output_file
        )
        
        return {
            "status": "success",
            "file_path": output_file,
            "message": "Investor statement generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/funds")
def list_funds():
    """List all funds"""
    import mysql.connector
    from config import DB_CONFIG
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT fund_id, fund_name, fund_type, vintage_year,
                   base_currency, total_committed_capital, fund_status
            FROM funds
            ORDER BY fund_name
        """)
        
        funds = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"funds": funds}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fund/{fund_id}/investors")
def list_fund_investors(fund_id: int):
    """List investors in a fund"""
    import mysql.connector
    from config import DB_CONFIG
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT i.investor_id, i.investor_name, i.investor_type,
                   ic.commitment_amount, ic.total_called,
                   ic.total_distributed, ic.ownership_percentage
            FROM investor_commitments ic
            JOIN investors i ON ic.investor_id = i.investor_id
            WHERE ic.fund_id = %s
            AND ic.status = 'active'
            ORDER BY ic.ownership_percentage DESC
        """, (fund_id,))
        
        investors = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"fund_id": fund_id, "investors": investors}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fund/{fund_id}/nav-history")
def get_nav_history(fund_id: int, limit: int = 12):
    """Get historical NAV calculations"""
    import mysql.connector
    from config import DB_CONFIG
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT calculation_date, net_asset_value,
                   tvpi, dpi, rvpi, nav_currency,
                   approval_status
            FROM nav_calculations
            WHERE fund_id = %s
            ORDER BY calculation_date DESC
            LIMIT %s
        """, (fund_id, limit))
        
        history = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"fund_id": fund_id, "nav_history": history}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# Run Server
# =====================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("STARTING PE FUND NAV CALCULATOR API")
    print("="*60)
    print(f"API Documentation: http://localhost:{API_CONFIG['port']}/docs")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        reload=True
    )
