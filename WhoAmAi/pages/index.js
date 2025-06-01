import { useRouter } from 'next/router';
import Head from 'next/head';
import ChoiceButton from '../components/ChoiceButton';

export default function Home() {
  const router = useRouter();

  const handleOpen = () => {
    router.push('/choices');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <Head>
        <title>Welcome | Personal Website</title>
        <meta name="description" content="Welcome to my personal website" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex flex-col items-center justify-center w-full max-w-md mx-auto text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-8">Welcome</h1>
        <ChoiceButton
          onClick={handleOpen}
          isLarge={true}
          className="w-48 h-48 rounded-full text-2xl"
        >
          Open?
        </ChoiceButton>
      </main>
    </div>
  );
}
