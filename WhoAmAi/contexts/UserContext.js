import { createContext, useState, useContext } from 'react';

// Create the context
const UserContext = createContext();

// Create a provider component
export function UserProvider({ children }) {
  const [userChoice, setUserChoice] = useState(null);

  // Function to update the user's choice
  const updateUserChoice = (choice) => {
    setUserChoice(choice);
  };

  // Value to be provided to consuming components
  const value = {
    userChoice,
    updateUserChoice,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

// Custom hook to use the context
export function useUserContext() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUserContext must be used within a UserProvider');
  }
  return context;
}
