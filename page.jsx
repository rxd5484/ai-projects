'use client';
import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Layout from '../../components/Layout';

export default function Account() {
  const [activeTab, setActiveTab] = useState('profile');
  const [isProcessing, setIsProcessing] = useState(false);
  const [showTerms, setShowTerms] = useState(false);
  const searchParams = useSearchParams();
  const status = searchParams ? searchParams.get('status') : null;
  
  // User profile state (mock data)
  const [name, setName] = useState('John Doe');
  const [email, setEmail] = useState('john.doe@example.com');
  
  // Display status messages based on URL params
  useEffect(() => {
    if (status === 'success') {
      alert('Subscription updated successfully!');
    } else if (status === 'cancel') {
      alert('Subscription update canceled.');
    }
  }, [status]);
  
  const handleSaveProfile = (e) => {
    e.preventDefault();
    // Handle saving profile data
    alert('Profile saved!');
  };

  const handlePaymentSubmit = (e) => {
    e.preventDefault();
    setIsProcessing(true);
    
    // Simulate payment processing
    setTimeout(() => {
      setIsProcessing(false);
      alert('Payment processed successfully! You are now on the Pro plan.');
    }, 2000);
  };

  // Terms and Conditions Modal
  const TermsModal = () => (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-lg shadow-xl max-w-3xl w-full max-h-screen overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-700 flex justify-between items-center">
          <h3 className="text-lg font-medium text-white">Terms and Conditions</h3>
          <button 
            onClick={() => setShowTerms(false)}
            className="text-gray-400 hover:text-white"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="px-6 py-4 text-gray-300 space-y-4 text-sm">
          <section>
            <h4 className="text-white font-medium text-base">1. Introduction</h4>
            <p>Welcome to AI Content Assistant ("we," "our," or "us"). By subscribing to our service, you are agreeing to be bound by these Terms and Conditions. Please read them carefully.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">2. Subscription Terms</h4>
            <p>Your subscription to the Pro plan will be billed at $20 per month. Payments are processed securely through our payment processor. By subscribing, you authorize us to charge your payment method on a recurring monthly basis until you cancel your subscription.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">3. Subscription Benefits</h4>
            <div className="mt-1">
              The Pro subscription includes:
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>Unlimited content generations</li>
                <li>Advanced content optimization features</li>
                <li>SEO recommendations</li>
                <li>Plagiarism checking</li>
                <li>Priority customer support</li>
              </ul>
            </div>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">4. Cancellation Policy</h4>
            <p>You may cancel your subscription at any time from your account settings page. Upon cancellation, you will continue to have access to Pro features until the end of your current billing cycle. No refunds will be provided for partial billing periods.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">5. Content Usage</h4>
            <p>You retain all rights to the content you generate using our platform. However, we are not responsible for any copyright infringement that may result from your use of our service. You are solely responsible for ensuring that your use of generated content complies with applicable laws and regulations.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">6. Service Availability</h4>
            <p>We strive to provide uninterrupted service, but we do not guarantee that the service will be available at all times. We reserve the right to modify, suspend, or discontinue the service at any time without notice.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">7. Rate Limiting</h4>
            <p>Even with unlimited generations, we implement reasonable rate limits to prevent abuse of our system. These limits are designed to allow normal usage patterns while preventing automated scraping or other forms of abuse.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">8. Privacy Policy</h4>
            <p>Our Privacy Policy governs the collection and use of your personal information. By using our service, you consent to the practices described in our Privacy Policy.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">9. Changes to Terms</h4>
            <p>We reserve the right to modify these Terms and Conditions at any time. If we make material changes, we will notify you via email or through the platform. Your continued use of the service after such modifications constitutes your acceptance of the updated terms.</p>
          </section>
          
          <section>
            <h4 className="text-white font-medium text-base">10. Contact Us</h4>
            <p>If you have any questions about these Terms and Conditions, please contact us at support@aicontentassistant.com.</p>
          </section>
        </div>
        <div className="px-6 py-4 border-t border-gray-700 flex justify-end">
          <button
            onClick={() => setShowTerms(false)}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            I Understand
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <Layout>
      {showTerms && <TermsModal />}
      
      <div className="bg-gray-900 min-h-screen py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-semibold text-white mb-6">Account Settings</h1>
          
          {/* Tabs */}
          <div className="border-b border-gray-700">
            <nav className="-mb-px flex space-x-8" aria-label="Tabs">
              <button
                onClick={() => setActiveTab('profile')}
                className={`${
                  activeTab === 'profile'
                    ? 'border-indigo-500 text-indigo-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Profile
              </button>
              <button
                onClick={() => setActiveTab('subscription')}
                className={`${
                  activeTab === 'subscription'
                    ? 'border-indigo-500 text-indigo-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Subscription
              </button>
              <button
                onClick={() => setActiveTab('billing')}
                className={`${
                  activeTab === 'billing'
                    ? 'border-indigo-500 text-indigo-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Billing
              </button>
            </nav>
          </div>
          
          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="mt-6">
              <div className="bg-gray-800 shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Profile Information</h3>
                  <div className="mt-5">
                    <form onSubmit={handleSaveProfile}>
                      <div className="grid grid-cols-6 gap-6">
                        <div className="col-span-6 sm:col-span-3">
                          <label htmlFor="name" className="block text-sm font-medium text-gray-300">
                            Full Name
                          </label>
                          <input
                            type="text"
                            name="name"
                            id="name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                        
                        <div className="col-span-6 sm:col-span-4">
                          <label htmlFor="email" className="block text-sm font-medium text-gray-300">
                            Email address
                          </label>
                          <input
                            type="email"
                            name="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                        
                        <div className="col-span-6">
                          <button
                            type="submit"
                            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                          >
                            Save
                          </button>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 bg-gray-800 shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Change Password</h3>
                  <div className="mt-5">
                    <form>
                      <div className="grid grid-cols-6 gap-6">
                        <div className="col-span-6 sm:col-span-4">
                          <label htmlFor="current-password" className="block text-sm font-medium text-gray-300">
                            Current Password
                          </label>
                          <input
                            type="password"
                            name="current-password"
                            id="current-password"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                        
                        <div className="col-span-6 sm:col-span-4">
                          <label htmlFor="new-password" className="block text-sm font-medium text-gray-300">
                            New Password
                          </label>
                          <input
                            type="password"
                            name="new-password"
                            id="new-password"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                        
                        <div className="col-span-6 sm:col-span-4">
                          <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-300">
                            Confirm New Password
                          </label>
                          <input
                            type="password"
                            name="confirm-password"
                            id="confirm-password"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                        
                        <div className="col-span-6">
                          <button
                            type="submit"
                            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                          >
                            Update Password
                          </button>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Subscription Tab */}
          {activeTab === 'subscription' && (
            <div className="mt-6">
              <div className="bg-gray-800 shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Current Plan</h3>
                  <div className="mt-5">
                    <div className="rounded-md bg-gray-700 px-6 py-5 sm:flex sm:items-start sm:justify-between">
                      <div className="sm:flex sm:items-start">
                        <div className="mt-3 sm:mt-0 sm:ml-4">
                          <div className="text-sm font-medium text-white">Free Plan</div>
                          <div className="mt-1 text-sm text-gray-300 sm:flex sm:items-center">
                            <div>5 generations per day</div>
                            <span className="hidden sm:mx-2 sm:inline" aria-hidden="true">
                              &middot;
                            </span>
                            <div className="mt-1 sm:mt-0">Limited features</div>
                          </div>
                        </div>
                      </div>
                      <div className="mt-4 sm:mt-0 sm:ml-6 sm:flex-shrink-0">
                        <button
                          type="button"
                          onClick={() => setActiveTab('billing')} // This will switch to the billing tab
                          className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm"
                        >
                          Upgrade to Pro
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 bg-gray-800 shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Available Plans</h3>
                  <div className="mt-5 space-y-6">
                    {/* Pro Plan */}
                    <div className="rounded-md bg-gray-700 px-6 py-5 border border-gray-600 sm:flex sm:items-start sm:justify-between">
                      <div className="sm:flex sm:items-start">
                        <div className="mt-3 sm:mt-0 sm:ml-4">
                          <div className="text-sm font-medium text-white">Pro Plan</div>
                          <div className="mt-1 text-sm text-gray-300">$20/month</div>
                          <div className="mt-2 text-sm text-gray-400">
                            <ul className="list-disc pl-5 space-y-1">
                              <li>Unlimited generations</li>
                              <li>Advanced content optimization</li>
                              <li>SEO recommendations</li>
                              <li>Plagiarism checking</li>
                              <li>Priority support</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                      <div className="mt-4 sm:mt-0 sm:ml-6 sm:flex-shrink-0">
                        <button
                          type="button"
                          onClick={() => setActiveTab('billing')} // This will switch to the billing tab
                          className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm"
                        >
                          Select Plan
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Billing Tab */}
          {activeTab === 'billing' && (
            <div className="mt-6">
              <div className="bg-gray-800 shadow sm:rounded-lg mb-6">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Complete Your Upgrade</h3>
                  <p className="mt-1 text-sm text-gray-300">
                    Enter your payment details to upgrade to the Pro plan at $20/month.
                  </p>
                </div>
              </div>

              <div className="bg-gray-800 shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Payment Information</h3>
                  <div className="mt-5">
                    <form className="space-y-6" onSubmit={handlePaymentSubmit}>
                      {/* Credit Card Details */}
                      <div>
                        <label htmlFor="card-number" className="block text-sm font-medium text-gray-300">
                          Card Number
                        </label>
                        <div className="mt-1">
                          <input
                            type="text"
                            id="card-number"
                            name="card-number"
                            placeholder="1234 5678 9012 3456"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-6">
                        <div className="col-span-2">
                          <label htmlFor="expiration" className="block text-sm font-medium text-gray-300">
                            Expiration Date
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              id="expiration"
                              name="expiration"
                              placeholder="MM / YY"
                              className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                            />
                          </div>
                        </div>

                        <div>
                          <label htmlFor="cvc" className="block text-sm font-medium text-gray-300">
                            CVC
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              id="cvc"
                              name="cvc"
                              placeholder="123"
                              className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Billing Address */}
                      <div>
                        <label htmlFor="name-on-card" className="block text-sm font-medium text-gray-300">
                          Name on Card
                        </label>
                        <div className="mt-1">
                          <input
                            type="text"
                            id="name-on-card"
                            name="name-on-card"
                            placeholder="John Doe"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                      </div>

                      <div>
                        <label htmlFor="address" className="block text-sm font-medium text-gray-300">
                          Billing Address
                        </label>
                        <div className="mt-1">
                          <input
                            type="text"
                            id="address"
                            name="address"
                            placeholder="123 Main St"
                            className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-6">
                        <div>
                          <label htmlFor="city" className="block text-sm font-medium text-gray-300">
                            City
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              id="city"
                              name="city"
                              placeholder="New York"
                              className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                            />
                          </div>
                        </div>

                        <div>
                          <label htmlFor="zip" className="block text-sm font-medium text-gray-300">
                            Zip Code
                          </label>
                          <div className="mt-1">
                            <input
                              type="text"
                              id="zip"
                              name="zip"
                              placeholder="12345"
                              className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-600 bg-gray-700 text-white rounded-md"
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center">
                        <input
                          id="terms"
                          name="terms"
                          type="checkbox"
                          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                        />
                        <label htmlFor="terms" className="ml-2 block text-sm text-gray-300">
                          I agree to the{' '}
                          <button
                            type="button"
                            onClick={() => setShowTerms(true)}
                            className="text-indigo-400 hover:text-indigo-300 underline"
                          >
                            Terms of Service
                          </button>
                          {' '}and authorize recurring monthly charges
                        </label>
                      </div>

                      <div>
                        <button
                          type="submit"
                          disabled={isProcessing}
                          className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                            isProcessing 
                              ? 'bg-indigo-400 cursor-not-allowed' 
                              : 'bg-indigo-600 hover:bg-indigo-700'
                          } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
                        >
                          {isProcessing ? 'Processing...' : 'Upgrade to Pro - $20/month'}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>

              <div className="mt-6 bg-gray-800 shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Payment Method</h3>
                  <div className="mt-5">
                    <div className="rounded-md bg-gray-700 px-6 py-5">
                      <div className="text-sm text-gray-300">
                        No payment method added yet.
                      </div>
                      <div className="mt-4">
                        <button
                          type="button"
                          className="inline-flex items-center px-4 py-2 border border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-200 bg-gray-600 hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Add Payment Method
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 bg-gray-800 shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg leading-6 font-medium text-white">Billing History</h3>
                  <div className="mt-5">
                    <div className="text-sm text-gray-300">
                      No billing history available.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}