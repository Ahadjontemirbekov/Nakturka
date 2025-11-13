// DOM elementlarini olish
const modal = document.getElementById('success-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const closeModalIcon = document.querySelector('.close-modal');
const successAmount = document.getElementById('success-amount');
const progressBar = document.getElementById('progress-bar');
const errorMessage = document.getElementById('error-message');

// Bazadan UC miqdorini olish funksiyasi
async function getUcAmountFromDatabase() {
    try {
        // Bu yerda sizning haqiqiy API manzilingiz bo'ladi
        // Misol uchun:
        // const response = await fetch('https://sizning-api-manzilingiz.com/api/uc-amount');

        // Hozircha simulyatsiya qilamiz
        return await simulateDatabaseFetch();

    } catch (error) {
        console.error('Bazadan ma\'lumot olishda xatolik:', error);
        throw error;
    }
}

// Bazadan olishni simulyatsiya qilish
async function simulateDatabaseFetch() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // 90% holatda muvaffaqiyatli, 10% holatda xato
            if (Math.random() > 0.1) {
                // Bazadan olingan haqiqiy ma'lumot
                const ucAmount = 100; // Bu qiymat bazadan keladi
                resolve(ucAmount);
            } else {
                reject(new Error('Server xatosi'));
            }
        }, 1500); // 1.5 soniya kutish (simulyatsiya)
    });
}

// Modalni ochish funksiyasi
async function openModal() {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Progress barni boshlash
    animateProgressBar();

    try {
        // Bazadan UC miqdorini olish
        const ucAmount = await getUcAmountFromDatabase();

        // UC miqdorini animatsiya bilan ko'rsatish
        animateValue(successAmount, 0, ucAmount, 2000);

        // Konfetti effektini ishga tushirish
        createConfetti();

        // Xato xabarini yashirish
        errorMessage.style.display = 'none';

    } catch (error) {
        // Xato holatida
        console.error('Xatolik:', error);
        errorMessage.style.display = 'block';
        successAmount.textContent = '0';
    }
}

// Modalni yopish funksiyasi
function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Raqamni animatsiya bilan o'zgartirish
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value.toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Progress barni animatsiya qilish
function animateProgressBar() {
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            progressBar.style.width = width + '%';
        }
    }, 50);
}

// Konfetti effektini yaratish
function createConfetti() {
    const colors = ['#f94144', '#f3722c', '#f8961e', '#f9c74f', '#90be6d', '#43aa8b', '#577590'];
    const confettiCount = 150;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';

        // Tasodifiy xususiyatlar
        const color = colors[Math.floor(Math.random() * colors.length)];
        const size = Math.random() * 10 + 5;
        const left = Math.random() * 100;
        const animationDuration = Math.random() * 3 + 2;

        // CSS xususiyatlarini o'rnatish
        confetti.style.backgroundColor = color;
        confetti.style.width = `${size}px`;
        confetti.style.height = `${size}px`;
        confetti.style.left = `${left}%`;
        confetti.style.animationDuration = `${animationDuration}s`;

        // Modalga qo'shish
        modal.appendChild(confetti);

        // Konfettini olib tashlash
        setTimeout(() => {
            confetti.remove();
        }, animationDuration * 1000);
    }
}

// Event listener'lar
closeModalBtn.addEventListener('click', closeModal);
closeModalIcon.addEventListener('click', closeModal);

// Tashqariga bosganda modalni yopish
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        closeModal();
    }
});

// ESC tugmasi bilan modalni yopish
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modal.style.display === 'flex') {
        closeModal();
    }
});

// Sahifa yuklanganda modalni avtomatik ochish
window.addEventListener('load', () => {
    setTimeout(openModal, 500);
});

// UC miqdorini yangilash (tashqi funksiya sifatida)
function updateUcAmount(newAmount) {
    const currentAmount = parseInt(successAmount.textContent.replace(/,/g, ''));
    animateValue(successAmount, currentAmount, newAmount, 1000);
}

// Progress barni qayta boshlash
function resetProgressBar() {
    progressBar.style.width = '0%';
}

// HAQIQIY API ULASH UCHUN KOD
// Quyidagi funksiyani o'z API manzilingizga moslashtiring:

/*
async function getRealUcAmount() {
    try {
        const response = await fetch('https://sizning-api-manzilingiz.com/api/uc-amount', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer sizning-tokeningiz' // Agar kerak bo'lsa
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data.ucAmount; // API javobidagi UC miqdori

    } catch (error) {
        console.error('API xatosi:', error);
        throw error;
    }
}
*/

// Konsolga modalni boshqarish funksiyalari
console.log("Modal boshqaruv funksiyalari:");
console.log("- openModal() - Modalni ochish");
console.log("- closeModal() - Modalni yopish");
console.log("- updateUcAmount(amount) - UC miqdorini yangilash");
console.log("- getUcAmountFromDatabase() - Bazadan UC miqdorini olish");