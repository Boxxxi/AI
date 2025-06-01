// Course Data
const courses = [
    {
        id: 'ds1001',
        title: 'Introduction to Data Science',
        category: 'core',
        description: 'Fundamentals of data science, including data collection, cleaning, and basic analysis.',
        level: 1,
        xp: 100,
        flashcards: [
            { question: 'What is data science?', answer: 'Data science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data.' },
            { question: 'What are the main steps in the data science process?', answer: '1. Problem definition 2. Data collection 3. Data cleaning 4. Data exploration 5. Model building 6. Model evaluation 7. Deployment' },
            { question: 'What is the difference between supervised and unsupervised learning?', answer: 'Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data.' }
        ]
    },
    {
        id: 'ds1002',
        title: 'Python for Data Science',
        category: 'core',
        description: 'Learn Python programming fundamentals and data science libraries like NumPy and Pandas.',
        level: 1,
        xp: 100,
        flashcards: [
            { question: 'What is NumPy?', answer: 'NumPy is a Python library for numerical computing that provides support for large, multi-dimensional arrays and matrices.' },
            { question: 'What is Pandas?', answer: 'Pandas is a Python library for data manipulation and analysis, providing data structures like DataFrames.' },
            { question: 'What is a DataFrame?', answer: 'A DataFrame is a 2-dimensional labeled data structure with columns of potentially different types, similar to a spreadsheet.' }
        ]
    },
    {
        id: 'ds2001',
        title: 'Machine Learning Fundamentals',
        category: 'ai',
        description: 'Introduction to machine learning algorithms and their applications in data science.',
        level: 2,
        xp: 200,
        flashcards: [
            { question: 'What is machine learning?', answer: 'Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.' },
            { question: 'What is overfitting?', answer: 'Overfitting occurs when a model learns the training data too well, including noise and outliers, leading to poor generalization.' },
            { question: 'What is cross-validation?', answer: 'Cross-validation is a technique for assessing how well a model will generalize to an independent dataset.' }
        ]
    },
    {
        id: 'ds2002',
        title: 'Deep Learning',
        category: 'ai',
        description: 'Advanced neural networks and deep learning techniques for complex data analysis.',
        level: 2,
        xp: 200,
        flashcards: [
            { question: 'What is a neural network?', answer: 'A neural network is a series of algorithms that attempts to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates.' },
            { question: 'What is backpropagation?', answer: 'Backpropagation is an algorithm used to train neural networks by calculating the gradient of the loss function with respect to the weights.' },
            { question: 'What is a convolutional neural network?', answer: 'A CNN is a type of deep neural network commonly used for analyzing visual imagery.' }
        ]
    },
    {
        id: 'ds3001',
        title: 'Data Ethics and Privacy',
        category: 'industry',
        description: 'Understanding ethical considerations and privacy concerns in data science.',
        level: 3,
        xp: 300,
        flashcards: [
            { question: 'What is data privacy?', answer: 'Data privacy refers to the proper handling of sensitive data including personal information.' },
            { question: 'What is GDPR?', answer: 'The General Data Protection Regulation is a regulation in EU law on data protection and privacy.' },
            { question: 'What are the main ethical concerns in data science?', answer: '1. Privacy 2. Bias 3. Transparency 4. Accountability 5. Fairness' }
        ]
    }
];

// Achievements Data
const achievements = [
    {
        id: 'first_course',
        title: 'First Course',
        description: 'Complete your first course',
        icon: 'fa-graduation-cap',
        unlocked: false
    },
    {
        id: 'flashcard_master',
        title: 'Flashcard Master',
        description: 'Master 100 flashcards',
        icon: 'fa-brain',
        unlocked: false
    },
    {
        id: 'streak_7',
        title: '7-Day Streak',
        description: 'Study for 7 days in a row',
        icon: 'fa-fire',
        unlocked: false
    },
    {
        id: 'ai_path',
        title: 'AI Path',
        description: 'Complete the AI research path',
        icon: 'fa-robot',
        unlocked: false
    }
];

// User Data
let userData = {
    name: 'Student',
    level: 1,
    xp: 0,
    xpToNextLevel: 100,
    completedCourses: [],
    masteredFlashcards: 0,
    currentStreak: 0,
    lastStudyDate: null,
    achievements: []
}; 