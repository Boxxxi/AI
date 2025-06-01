import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import ChoiceButton from '../components/ChoiceButton';
import { useUserContext } from '../utils/UserContext';

export default function Choices() {
  const router = useRouter();
  const { updateUserChoice } = useUserContext();
  const [selectedChoice, setSelectedChoice] = useState(null);
  const [redirecting, setRedirecting] = useState(false);

  const handleChoiceClick = (choice) => {
    if (!redirecting) {
      setSelectedChoice(choice);
      updateUserChoice(choice);
      setRedirecting(true);
      
      // Wait for 2 seconds before redirecting
      setTimeout(() => {
        router.push('/final');
      }, 2000);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <Head>
        <title>Choose Your Path | Personal Website</title>
        <meta name="description" content="Choose your path on my personal website" />
      </Head>

      <main className="flex flex-col items-center justify-center w-full max-w-lg mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Make a Choice</h1>
        
        <div className="flex flex-col w-full space-y-6">
          <ChoiceButton 
            onClick={() => handleChoiceClick('game')} 
            disabled={redirecting}
            isLarge={true}
            className={selectedChoice === 'game' ? 'ring-4 ring-blue-500' : ''}
          >
            Play a Game?
          </ChoiceButton>
          
          <ChoiceButton 
            onClick={() => handleChoiceClick('ml')} 
            disabled={redirecting}
            isLarge={true}
            className={selectedChoice === 'ml' ? 'ring-4 ring-blue-500' : ''}
          >
            Another Washed-up ML Project? (Or is it?)
          </ChoiceButton>
          
          <ChoiceButton 
            onClick={() => handleChoiceClick('mystery')} 
            disabled={redirecting}
            isLarge={true}
            className={`flex items-center justify-center ${selectedChoice === 'mystery' ? 'ring-4 ring-blue-500' : ''}`}
          >
            <svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </ChoiceButton>
        </div>
        
        {redirecting && (
          <p className="mt-8 text-blue-500 animate-pulse">
            Your choice has been made... redirecting...
          </p>
        )}
      </main>
    </div>
  );
}
