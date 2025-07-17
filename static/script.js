document.addEventListener('DOMContentLoaded', () => {
    const imageInputs = document.querySelectorAll('.image-input');
    const scaleSliders = document.querySelectorAll('.scale-slider');
    const generateBtn = document.getElementById('generate-btn');
    const resultArea = document.getElementById('result-area');
    const resultImage = document.getElementById('result-image');
    const downloadLink = document.getElementById('download-link');

    const files = {};
    const scales = {
        top_left: 1, top_right: 1,
        bottom_left: 1, bottom_right: 1
    };

    // Gestionează încărcarea imaginilor și afișarea previzualizării
    imageInputs.forEach(input => {
        input.addEventListener('change', (event) => {
            const position = event.target.dataset.position;
            const file = event.target.files[0];
            if (file) {
                files[position] = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    const previewBox = document.getElementById(`preview_${position}`);
                    previewBox.innerHTML = ''; // Golește textul "Imagine X"
                    let img = previewBox.querySelector('img');
                    if (!img) {
                        img = document.createElement('img');
                        previewBox.appendChild(img);
                    }
                    img.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Gestionează sliderele de scalare
    scaleSliders.forEach(slider => {
        slider.addEventListener('input', (event) => {
            const position = event.target.dataset.position;
            const scaleValue = event.target.value;
            scales[position] = scaleValue;

            const previewBox = document.getElementById(`preview_${position}`);
            const img = previewBox.querySelector('img');
            if (img) {
                img.style.transform = `scale(${scaleValue})`;
            }

            // --- MODIFICARE: Actualizăm valoarea afișată ---
            // Găsim elementul span de lângă slider-ul curent
            const valueSpan = event.target.parentElement.querySelector('.scale-value');
            if (valueSpan) {
                // Afișăm valoarea formatată cu două zecimale
                valueSpan.textContent = parseFloat(scaleValue).toFixed(2);
            }
            // ------------------------------------------------
        });
    });

    // Gestionează butonul de generare
    generateBtn.addEventListener('click', async () => {
        if (Object.keys(files).length !== 4) {
            alert('Te rog încarcă toate cele 4 imagini!');
            return;
        }

        generateBtn.textContent = 'Se generează...';
        generateBtn.disabled = true;
        resultArea.classList.add('hidden');

        const formData = new FormData();
        for (const position in files) {
            formData.append(`image_${position}`, files[position]);
            formData.append(`scale_${position}`, scales[position]);
        }

        try {
            const response = await fetch('/api/generate-collage', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Eroare de la server: ${errorText}`);
            }

            const imageBlob = await response.blob();
            const imageUrl = URL.createObjectURL(imageBlob);

            resultImage.src = imageUrl;
            downloadLink.href = imageUrl;
            downloadLink.download = `colaj_final_${Date.now()}.png`;
            resultArea.classList.remove('hidden');

        } catch (error) {
            console.error('Eroare la generarea colajului:', error);
            alert(`A apărut o eroare: ${error.message}`);
        } finally {
            generateBtn.textContent = 'Generează Colaj';
            generateBtn.disabled = false;
        }
    });
});
