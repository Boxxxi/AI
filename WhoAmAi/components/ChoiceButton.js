import { useState } from 'react';

export default function ChoiceButton({ onClick, disabled = false, children, isLarge = false, className = '' }) {
  const [isPressed, setIsPressed] = useState(false);

  const handleClick = () => {
    if (!disabled) {
      setIsPressed(true);
      onClick();
    }
  };

  const baseStyles = `
    inline-flex items-center justify-center 
    rounded-md font-medium transition-all 
    focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2
    ${disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'}
    ${isPressed ? 'bg-blue-700 text-white' : 'bg-blue-500 text-white hover:bg-blue-600 active:bg-blue-700'}
    ${isLarge ? 'px-8 py-4 text-xl md:text-2xl' : 'px-6 py-3 text-base'}
    glow-effect
  `;

  return (
    <button
      onClick={handleClick}
      disabled={disabled}
      className={`${baseStyles} ${className}`}
    >
      {children}
    </button>
  );
}
