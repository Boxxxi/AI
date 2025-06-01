import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import ChoiceButton from '../components/ChoiceButton';
import { useUserContext } from '../utils/UserContext';

export default function Final() {
  const router = useRouter();
  const { userChoice } = useUserContext();
  const [message, setMessage] = useState("");
  const [title, setTitle] = useState("");

  useEffect(() => {
    // Define messages based on user choice
    if (userChoice === 'game') {
      setTitle("Game Selected!");
      setMessage("You've chosen to play a game! Unfortunately, the game development is still in progress. Check back soon for an amazing gaming experience!");
    } else if (userChoice === 'ml') {
      setTitle("ML Project Selected!");
      setMessage("Ah, interested in machine learning? This isn't just another washed-up ML project. It's a journey into the future of AI and what it can accomplish. Stay tuned for updates!");
    } else if (userChoice === 'mystery') {
      setTitle("Mystery Awaits!");
      setMessage("Curiosity led you to choose the unknown. That's the mark of an adventurer! The mystery will unfold soon. Keep exploring!");
    } else {
      setTitle("The Unknown Path");
      setMessage("You explored the unknown. No choice was made, yet here you are. Sometimes the journey itself is the destination.");
    }
  }, [userChoice]);

  const handleGoHome = () => {
    router.push('/');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <Head>
        <title>{title || "Final Page"} | Personal Website</title>
        <meta name="description" content="The final page of your journey" />
      </Head>

      <main className="flex flex-col items-center justify-center w-full max-w-2xl mx-auto text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">{title}</h1>
        
        <div className="bg-white shadow-lg rounded-lg p-8 mb-8">
          <p className="text-xl text-gray-700 mb-6">{message}</p>
        </div>
        
        <ChoiceButton onClick={handleGoHome}>
          Return Home
        </ChoiceButton>
      </main>
    </div>
  );
}
