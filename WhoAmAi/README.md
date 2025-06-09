# WhoAmAi

A Next.js application for interactive AI personality assessment.

## Description

WhoAmAi is a web application that helps users assess their personality through an interactive experience. The app provides choices and generates personalized results based on user responses.

## Features

- Interactive personality assessment
- Modern UI with Tailwind CSS
- Responsive design
- Dynamic personality analysis
- Real-time feedback

## Project Structure

```
WhoAmAi/
├── components/          # Reusable UI components
│   └── ChoiceButton.js  # Custom button component for choices
├── contexts/           # React context providers
│   └── UserContext.js  # User state management
├── pages/              # Next.js pages
│   ├── _app.js         # Custom App component
│   ├── _document.js    # Custom Document component
│   ├── index.js        # Landing page
│   ├── choices.js      # Question/choice interface
│   └── final.js        # Results page
├── styles/             # Global styles and Tailwind config
├── utils/              # Utility functions
└── public/            # Static assets
```

## Technologies Used

- Next.js - React framework for production
- React - UI library
- Tailwind CSS - Utility-first CSS framework
- JavaScript - Programming language

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/WhoAmAi.git
cd WhoAmAi
```

2. Install dependencies
```bash
npm install
# or
yarn install
```

3. Run the development server
```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run test` - Run tests

### Code Style

This project uses:
- ESLint for code linting
- Prettier for code formatting
- Tailwind CSS for styling

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details. 