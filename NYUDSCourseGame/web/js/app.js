// DOM Elements
const views = {
    home: document.getElementById('homeView'),
    courses: document.getElementById('coursesView'),
    aiPath: document.getElementById('aiPathView'),
    flashcards: document.getElementById('flashcardView'),
    profile: document.getElementById('profileView')
};

const userInfo = {
    name: document.getElementById('userName'),
    level: document.getElementById('userLevel'),
    progress: document.getElementById('levelProgress')
};

// Navigation
document.querySelectorAll('.nav-btn').forEach(button => {
    button.addEventListener('click', () => {
        const targetView = button.dataset.view;
        showView(targetView);
    });
});

document.querySelectorAll('.back-btn').forEach(button => {
    button.addEventListener('click', () => {
        showView('home');
    });
});

// View Management
function showView(viewName) {
    Object.values(views).forEach(view => view.classList.remove('active'));
    views[viewName].classList.add('active');
    
    switch(viewName) {
        case 'courses':
            renderCourses();
            break;
        case 'aiPath':
            renderAIPath();
            break;
        case 'profile':
            renderProfile();
            break;
    }
}

// Course Management
function renderCourses() {
    const coursesGrid = document.getElementById('coursesGrid');
    coursesGrid.innerHTML = '';
    
    const searchTerm = document.getElementById('courseSearch').value.toLowerCase();
    const activeCategory = document.querySelector('.pill.active').dataset.category;
    
    courses.forEach(course => {
        if ((activeCategory === 'all' || course.category === activeCategory) &&
            (course.title.toLowerCase().includes(searchTerm) || 
             course.description.toLowerCase().includes(searchTerm))) {
            
            const courseCard = document.createElement('div');
            courseCard.className = 'course-card';
            courseCard.innerHTML = `
                <h3>${course.title}</h3>
                <p>${course.description}</p>
                <div class="course-info">
                    <span>Level ${course.level}</span>
                    <span>${course.xp} XP</span>
                </div>
            `;
            
            courseCard.addEventListener('click', () => {
                startFlashcardSession(course);
            });
            
            coursesGrid.appendChild(courseCard);
        }
    });
}

// Category Filter
document.querySelectorAll('.pill').forEach(pill => {
    pill.addEventListener('click', () => {
        document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        renderCourses();
    });
});

// Search Functionality
document.getElementById('courseSearch').addEventListener('input', renderCourses);

// Flashcard System
let currentCourse = null;
let currentFlashcards = [];
let currentCardIndex = 0;

function startFlashcardSession(course) {
    currentCourse = course;
    currentFlashcards = [...course.flashcards];
    currentCardIndex = 0;
    
    document.getElementById('currentCourseTitle').textContent = course.title;
    document.getElementById('cardsRemaining').textContent = `0/${currentFlashcards.length}`;
    document.getElementById('studyProgress').style.width = '0%';
    
    showView('flashcards');
    showNextCard();
}

function showNextCard() {
    if (currentCardIndex >= currentFlashcards.length) {
        // Session complete
        showView('home');
        return;
    }
    
    const card = currentFlashcards[currentCardIndex];
    document.getElementById('cardQuestion').textContent = card.question;
    document.getElementById('cardAnswer').textContent = card.answer;
    document.getElementById('currentCard').classList.remove('flipped');
    
    document.getElementById('cardsRemaining').textContent = 
        `${currentCardIndex}/${currentFlashcards.length}`;
    document.getElementById('studyProgress').style.width = 
        `${(currentCardIndex / currentFlashcards.length) * 100}%`;
}

// Flashcard Controls
document.getElementById('flipBtn').addEventListener('click', () => {
    document.getElementById('currentCard').classList.toggle('flipped');
});

document.getElementById('wrongBtn').addEventListener('click', () => {
    currentCardIndex++;
    showNextCard();
});

document.getElementById('correctBtn').addEventListener('click', () => {
    userData.masteredFlashcards++;
    currentCardIndex++;
    showNextCard();
    checkAchievements();
});

// AI Path
function renderAIPath() {
    const sections = {
        core: document.getElementById('coreCourses'),
        ai: document.getElementById('aiSkillsCourses'),
        specialized: document.getElementById('specializedCourses'),
        industry: document.getElementById('industryCourses')
    };
    
    Object.keys(sections).forEach(section => {
        sections[section].innerHTML = '';
        const sectionCourses = courses.filter(course => course.category === section);
        
        sectionCourses.forEach(course => {
            const courseElement = document.createElement('div');
            courseElement.className = 'path-course';
            courseElement.innerHTML = `
                <h4>${course.title}</h4>
                <p>${course.description}</p>
            `;
            sections[section].appendChild(courseElement);
        });
    });
}

// Profile Management
function renderProfile() {
    document.getElementById('profileName').textContent = userData.name;
    document.getElementById('profileLevel').textContent = userData.level;
    document.getElementById('profileProgress').style.width = 
        `${(userData.xp / userData.xpToNextLevel) * 100}%`;
    
    document.getElementById('coursesCompleted').textContent = userData.completedCourses.length;
    document.getElementById('flashcardsMastered').textContent = userData.masteredFlashcards;
    document.getElementById('currentStreak').textContent = userData.currentStreak;
    document.getElementById('achievementsUnlocked').textContent = userData.achievements.length;
    
    renderAchievements();
}

function renderAchievements() {
    const achievementsGrid = document.getElementById('achievementsGrid');
    achievementsGrid.innerHTML = '';
    
    achievements.forEach(achievement => {
        const achievementCard = document.createElement('div');
        achievementCard.className = `achievement-card ${achievement.unlocked ? 'unlocked' : 'locked'}`;
        achievementCard.innerHTML = `
            <i class="fas ${achievement.icon}"></i>
            <h4>${achievement.title}</h4>
            <p>${achievement.description}</p>
        `;
        achievementsGrid.appendChild(achievementCard);
    });
}

// Achievement System
function checkAchievements() {
    // First Course Achievement
    if (userData.completedCourses.length === 1 && !achievements[0].unlocked) {
        unlockAchievement('first_course');
    }
    
    // Flashcard Master Achievement
    if (userData.masteredFlashcards >= 100 && !achievements[1].unlocked) {
        unlockAchievement('flashcard_master');
    }
    
    // 7-Day Streak Achievement
    if (userData.currentStreak >= 7 && !achievements[2].unlocked) {
        unlockAchievement('streak_7');
    }
    
    // AI Path Achievement
    const aiCourses = courses.filter(course => course.category === 'ai');
    if (aiCourses.every(course => userData.completedCourses.includes(course.id)) && !achievements[3].unlocked) {
        unlockAchievement('ai_path');
    }
}

function unlockAchievement(achievementId) {
    const achievement = achievements.find(a => a.id === achievementId);
    if (achievement && !achievement.unlocked) {
        achievement.unlocked = true;
        userData.achievements.push(achievementId);
        showAchievementNotification(achievement);
        renderProfile();
    }
}

function showAchievementNotification(achievement) {
    const notification = document.createElement('div');
    notification.className = 'achievement-notification';
    notification.innerHTML = `
        <i class="fas ${achievement.icon}"></i>
        <div>
            <h4>Achievement Unlocked!</h4>
            <p>${achievement.title}</p>
        </div>
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Initialize
function init() {
    // Load user data from localStorage if available
    const savedData = localStorage.getItem('userData');
    if (savedData) {
        userData = JSON.parse(savedData);
    }
    
    // Update UI
    userInfo.name.textContent = userData.name;
    userInfo.level.textContent = userData.level;
    userInfo.progress.style.width = `${(userData.xp / userData.xpToNextLevel) * 100}%`;
    
    // Check streak
    const today = new Date().toDateString();
    if (userData.lastStudyDate !== today) {
        const lastStudy = new Date(userData.lastStudyDate);
        const todayDate = new Date();
        const diffTime = Math.abs(todayDate - lastStudy);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
            userData.currentStreak++;
        } else if (diffDays > 1) {
            userData.currentStreak = 0;
        }
        
        userData.lastStudyDate = today;
        saveUserData();
    }
}

// Save user data
function saveUserData() {
    localStorage.setItem('userData', JSON.stringify(userData));
}

// Start the application
document.addEventListener('DOMContentLoaded', init); 