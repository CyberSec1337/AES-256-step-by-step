// static/aes.js
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("aes-form");
    const resultDiv = document.getElementById("result");
    const animationDiv = document.getElementById("animation");
    const downloadLink = document.getElementById("download-link");
    const modeSelect = document.getElementById("mode-select");
    const ivSection = document.getElementById("iv-section");
    const keyInput = document.getElementById("key-input");
    const ivInput = document.getElementById("iv-input");
    const textInput = document.getElementById("text-input");
    const keyLengthSpan = document.getElementById("key-length");
    const ivLengthSpan = document.getElementById("iv-length");
    const textLengthSpan = document.getElementById("text-length");
    const textCharsSpan = document.getElementById("text-chars");
    const viewControls = document.getElementById("view-controls");
    const flowchartBtn = document.getElementById("flowchart-btn");
    const stepsBtn = document.getElementById("steps-btn");
    const flowchartContainer = document.getElementById("flowchart-container");
    
    // Language elements
    const langEnBtn = document.getElementById("lang-en");
    const langArBtn = document.getElementById("lang-ar");
    let currentLang = 'en';

    // Language switching functionality
    function switchLanguage(lang) {
        currentLang = lang;
        
        // Toggle language buttons
        if (lang === 'en') {
            langEnBtn.classList.add('active');
            langArBtn.classList.remove('active');
            
            // Show English elements
            document.getElementById('instructions-en').style.display = 'block';
            document.getElementById('text-label-en').style.display = 'block';
            document.getElementById('key-label-en').style.display = 'block';
            document.getElementById('mode-label-en').style.display = 'block';
            document.getElementById('iv-label-en').style.display = 'block';
            document.getElementById('buttons-en').style.display = 'block';
            document.getElementById('text-counter-en').style.display = 'inline';
            document.getElementById('key-counter-en').style.display = 'inline';
            document.getElementById('iv-counter-en').style.display = 'inline';
            document.getElementById('view-toggle-en').style.display = 'flex';
            document.getElementById('flowchart-title-en').style.display = 'block';
            
            // Hide Arabic elements
            document.getElementById('instructions-ar').style.display = 'none';
            document.getElementById('text-label-ar').style.display = 'none';
            document.getElementById('key-label-ar').style.display = 'none';
            document.getElementById('mode-label-ar').style.display = 'none';
            document.getElementById('iv-label-ar').style.display = 'none';
            document.getElementById('buttons-ar').style.display = 'none';
            document.getElementById('text-counter-ar').style.display = 'none';
            document.getElementById('key-counter-ar').style.display = 'none';
            document.getElementById('iv-counter-ar').style.display = 'none';
            document.getElementById('view-toggle-ar').style.display = 'none';
            document.getElementById('flowchart-title-ar').style.display = 'none';
            
            // Update placeholders
            textInput.placeholder = "Enter at least 16 bytes here...";
            keyInput.placeholder = "MySecretKey123456789012345678901";
            if (ivInput) ivInput.placeholder = "1234567890123456";
            
            // Show English flowchart labels
            showEnglishFlowchartLabels();
            
            // Update download link
            document.getElementById('download-text-en').style.display = 'inline';
            document.getElementById('download-text-ar').style.display = 'none';
            
        } else {
            langArBtn.classList.add('active');
            langEnBtn.classList.remove('active');
            
            // Show Arabic elements
            document.getElementById('instructions-ar').style.display = 'block';
            document.getElementById('text-label-ar').style.display = 'block';
            document.getElementById('key-label-ar').style.display = 'block';
            document.getElementById('mode-label-ar').style.display = 'block';
            document.getElementById('iv-label-ar').style.display = 'block';
            document.getElementById('buttons-ar').style.display = 'block';
            document.getElementById('text-counter-ar').style.display = 'inline';
            document.getElementById('key-counter-ar').style.display = 'inline';
            document.getElementById('iv-counter-ar').style.display = 'inline';
            document.getElementById('view-toggle-ar').style.display = 'flex';
            document.getElementById('flowchart-title-ar').style.display = 'block';
            
            // Hide English elements
            document.getElementById('instructions-en').style.display = 'none';
            document.getElementById('text-label-en').style.display = 'none';
            document.getElementById('key-label-en').style.display = 'none';
            document.getElementById('mode-label-en').style.display = 'none';
            document.getElementById('iv-label-en').style.display = 'none';
            document.getElementById('buttons-en').style.display = 'none';
            document.getElementById('text-counter-en').style.display = 'none';
            document.getElementById('key-counter-en').style.display = 'none';
            document.getElementById('iv-counter-en').style.display = 'none';
            document.getElementById('view-toggle-en').style.display = 'none';
            document.getElementById('flowchart-title-en').style.display = 'none';
            
            // Update placeholders
            textInput.placeholder = "أدخل 16 بايت على الأقل هنا...";
            keyInput.placeholder = "مفتاحي_السري_123456789012345678901";
            if (ivInput) ivInput.placeholder = "1234567890123456";
            
            // Show Arabic flowchart labels
            showArabicFlowchartLabels();
            
            // Update download link
            document.getElementById('download-text-en').style.display = 'none';
            document.getElementById('download-text-ar').style.display = 'inline';
        }
    }
    
    function showEnglishFlowchartLabels() {
        // Stage headers
        document.getElementById('stage-input-header-en').style.display = 'block';
        document.getElementById('stage-input-header-ar').style.display = 'none';
        document.getElementById('stage-key-header-en').style.display = 'block';
        document.getElementById('stage-key-header-ar').style.display = 'none';
        document.getElementById('stage-mode-header-en').style.display = 'block';
        document.getElementById('stage-mode-header-ar').style.display = 'none';
        document.getElementById('stage-processing-header-en').style.display = 'block';
        document.getElementById('stage-processing-header-ar').style.display = 'none';
        document.getElementById('stage-output-header-en').style.display = 'block';
        document.getElementById('stage-output-header-ar').style.display = 'none';
        
        // Box titles
        document.getElementById('input-box-title-en').style.display = 'block';
        document.getElementById('input-box-title-ar').style.display = 'none';
        document.getElementById('key-box-title-en').style.display = 'block';
        document.getElementById('key-box-title-ar').style.display = 'none';
        document.getElementById('mode-box-title-en').style.display = 'block';
        document.getElementById('mode-box-title-ar').style.display = 'none';
        document.getElementById('iv-box-title-en').style.display = 'block';
        document.getElementById('iv-box-title-ar').style.display = 'none';
        document.getElementById('output-box-title-en').style.display = 'block';
        document.getElementById('output-box-title-ar').style.display = 'none';
    }
    
    function showArabicFlowchartLabels() {
        // Stage headers
        document.getElementById('stage-input-header-en').style.display = 'none';
        document.getElementById('stage-input-header-ar').style.display = 'block';
        document.getElementById('stage-key-header-en').style.display = 'none';
        document.getElementById('stage-key-header-ar').style.display = 'block';
        document.getElementById('stage-mode-header-en').style.display = 'none';
        document.getElementById('stage-mode-header-ar').style.display = 'block';
        document.getElementById('stage-processing-header-en').style.display = 'none';
        document.getElementById('stage-processing-header-ar').style.display = 'block';
        document.getElementById('stage-output-header-en').style.display = 'none';
        document.getElementById('stage-output-header-ar').style.display = 'block';
        
        // Box titles
        document.getElementById('input-box-title-en').style.display = 'none';
        document.getElementById('input-box-title-ar').style.display = 'block';
        document.getElementById('key-box-title-en').style.display = 'none';
        document.getElementById('key-box-title-ar').style.display = 'block';
        document.getElementById('mode-box-title-en').style.display = 'none';
        document.getElementById('mode-box-title-ar').style.display = 'block';
        document.getElementById('iv-box-title-en').style.display = 'none';
        document.getElementById('iv-box-title-ar').style.display = 'block';
        document.getElementById('output-box-title-en').style.display = 'none';
        document.getElementById('output-box-title-ar').style.display = 'block';
    }
    
    // Language button event listeners
    langEnBtn.addEventListener('click', () => switchLanguage('en'));
    langArBtn.addEventListener('click', () => switchLanguage('ar'));

    // Show/hide IV section based on mode selection
    modeSelect.addEventListener("change", function() {
        const ivLabel = document.getElementById("iv-label");
        if (this.value === "ECB") {
            ivSection.style.display = "none";
        } else {
            ivSection.style.display = "block";
            // Update label based on mode
            if (this.value === "CTR") {
                ivLabel.textContent = "Nonce (exactly 16 characters):";
            } else {
                ivLabel.textContent = "IV (exactly 16 characters):";
            }
        }
    });

    // Update text length counter (bytes and characters)
    textInput.addEventListener("input", function() {
        const text = this.value;
        const byteLength = new TextEncoder().encode(text).length;
        const charLength = text.length;
        
        // Update English counters
        textLengthSpan.textContent = byteLength;
        textCharsSpan.textContent = charLength;
        
        // Update Arabic counters
        document.getElementById('text-length-ar').textContent = byteLength;
        document.getElementById('text-chars-ar').textContent = charLength;
        
        const color = byteLength >= 16 ? "#28a745" : "#dc3545";
        const weight = "bold";
        
        // Style English counters
        textLengthSpan.style.color = color;
        textLengthSpan.style.fontWeight = weight;
        
        // Style Arabic counters
        document.getElementById('text-length-ar').style.color = color;
        document.getElementById('text-length-ar').style.fontWeight = weight;
    });

    // Update key length counter
    keyInput.addEventListener("input", function() {
        const length = this.value.length;
        const color = length === 32 ? "#28a745" : "#dc3545";
        
        // Update English counter
        keyLengthSpan.textContent = length;
        keyLengthSpan.style.color = color;
        
        // Update Arabic counter
        document.getElementById('key-length-ar').textContent = length;
        document.getElementById('key-length-ar').style.color = color;
    });

    // Update IV length counter
    if (ivInput) {
        ivInput.addEventListener("input", function() {
            const length = this.value.length;
            const color = length === 16 ? "#28a745" : "#dc3545";
            
            // Update English counter
            ivLengthSpan.textContent = length;
            ivLengthSpan.style.color = color;
            
            // Update Arabic counter
            document.getElementById('iv-length-ar').textContent = length;
            document.getElementById('iv-length-ar').style.color = color;
        });
    }

    // View toggle functionality - English buttons
    flowchartBtn.addEventListener("click", function() {
        flowchartBtn.classList.add("active");
        stepsBtn.classList.remove("active");
        document.getElementById("flowchart-btn-ar").classList.add("active");
        document.getElementById("steps-btn-ar").classList.remove("active");
        flowchartContainer.style.display = "block";
        animationDiv.style.display = "none";
    });

    stepsBtn.addEventListener("click", function() {
        stepsBtn.classList.add("active");
        flowchartBtn.classList.remove("active");
        document.getElementById("steps-btn-ar").classList.add("active");
        document.getElementById("flowchart-btn-ar").classList.remove("active");
        flowchartContainer.style.display = "none";
        animationDiv.style.display = "block";
    });
    
    // View toggle functionality - Arabic buttons
    document.getElementById("flowchart-btn-ar").addEventListener("click", function() {
        document.getElementById("flowchart-btn-ar").classList.add("active");
        document.getElementById("steps-btn-ar").classList.remove("active");
        flowchartBtn.classList.add("active");
        stepsBtn.classList.remove("active");
        flowchartContainer.style.display = "block";
        animationDiv.style.display = "none";
    });

    document.getElementById("steps-btn-ar").addEventListener("click", function() {
        document.getElementById("steps-btn-ar").classList.add("active");
        document.getElementById("flowchart-btn-ar").classList.remove("active");
        stepsBtn.classList.add("active");
        flowchartBtn.classList.remove("active");
        flowchartContainer.style.display = "none";
        animationDiv.style.display = "block";
    });

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Client-side validation for 16-byte requirement
        const text = textInput.value;
        const byteLength = new TextEncoder().encode(text).length;
        
        if (byteLength < 16) {
            const errorMsg = currentLang === 'en' 
                ? `<div class="error"><strong>Error:</strong> Text must be at least 16 bytes long. Current length: ${byteLength} bytes. Please add more text.</div>`
                : `<div class="error"><strong>خطأ:</strong> يجب أن يكون النص 16 بايت على الأقل. الطول الحالي: ${byteLength} بايت. يرجى إضافة المزيد من النص.</div>`;
            resultDiv.innerHTML = errorMsg;
            return;
        }

        const formData = new FormData(form);
        const action = e.submitter.value;
        formData.append("action", action);

        const processingMsg = currentLang === 'en' ? "Processing..." : "جاري المعالجة...";
        resultDiv.innerHTML = processingMsg;
        animationDiv.innerHTML = "";
        downloadLink.style.display = "none";
        viewControls.style.display = "none";
        flowchartContainer.style.display = "none";

        const response = await fetch("/process", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<div class="error"><strong>Error:</strong> ${data.error}</div>`;
            return;
        }

        const outputLabel = currentLang === 'en' ? 'Output:' : 'النتيجة:';
        resultDiv.innerHTML = `<b>${outputLabel}</b> <code>${data.result}</code>`;
        
        // Show view controls
        viewControls.style.display = "block";
        
        // Show and populate flowchart (default view)
        showFlowchart(data.steps, data.result, action);
        
        // Prepare traditional step animation (hidden initially)
        animateSteps(data.steps);
        animationDiv.style.display = "none";
        
        downloadLink.style.display = "inline-block";
    });

    function showFlowchart(steps, result, action) {
        const flowchartContainer = document.getElementById("flowchart-container");
        const inputText = document.getElementById("input-text");
        const keyDisplay = document.getElementById("key-display");
        const modeDisplay = document.getElementById("mode-display");
        const ivDisplay = document.getElementById("iv-display");
        const ivDisplayBox = document.getElementById("iv-display-box");
        const outputText = document.getElementById("output-text");
        const blocksContainer = document.getElementById("blocks-container");

        // Get form values
        const formData = new FormData(document.getElementById("aes-form"));
        const inputValue = formData.get("text");
        const keyValue = formData.get("key");
        const modeValue = formData.get("mode");
        const ivValue = formData.get("iv");

        // Populate flowchart data
        inputText.textContent = inputValue.length > 50 ? inputValue.substring(0, 50) + "..." : inputValue;
        keyDisplay.textContent = keyValue;
        modeDisplay.textContent = modeValue + " Mode";
        outputText.textContent = result.length > 50 ? result.substring(0, 50) + "..." : result;

        // Show/hide IV based on mode
        if (modeValue === "ECB") {
            ivDisplayBox.style.display = "none";
        } else {
            ivDisplayBox.style.display = "block";
            const ivLabel = modeValue === "CTR" ? "Nonce" : "IV";
            document.querySelector("#iv-display-box .box-title").textContent = ivLabel;
            ivDisplay.textContent = ivValue || "Auto-generated";
        }

        // Clear previous blocks
        blocksContainer.innerHTML = "";

        // Create block processing visualization
        createBlockProcessing(steps, blocksContainer, action);

        // Show flowchart
        flowchartContainer.style.display = "block";

        // Animate stages
        animateFlowchartStages(steps);
    }

    function createBlockProcessing(steps, container, action) {
        // Find block-related steps
        const blockSteps = steps.filter(step => 
            step.step.includes("Block") || 
            step.step.includes("Encryption") || 
            step.step.includes("Decryption")
        );

        if (blockSteps.length === 0) return;

        // Group steps by block
        const blockGroups = {};
        blockSteps.forEach(step => {
            const blockMatch = step.step.match(/Block (\d+)/);
            if (blockMatch) {
                const blockNum = blockMatch[1];
                if (!blockGroups[blockNum]) {
                    blockGroups[blockNum] = [];
                }
                blockGroups[blockNum].push(step);
            }
        });

        // Create visual blocks
        Object.keys(blockGroups).forEach(blockNum => {
            const blockContainer = document.createElement("div");
            blockContainer.className = "block-container";
            blockContainer.innerHTML = `
                <div class="block-header">Block ${blockNum} Processing</div>
                <div class="block-steps" id="block-${blockNum}-steps"></div>
            `;
            container.appendChild(blockContainer);

            const stepsContainer = blockContainer.querySelector(`#block-${blockNum}-steps`);
            blockGroups[blockNum].forEach(step => {
                const stepEl = document.createElement("div");
                stepEl.className = "block-step";
                
                // Extract matrix data if available
                const lines = step.detail.split('\n');
                let content = step.step;
                
                // Look for hex data
                const hexMatch = step.detail.match(/([A-F0-9]{32,})/);
                if (hexMatch) {
                    content += `<br><div class="matrix-display">${formatAsMatrix(hexMatch[1])}</div>`;
                }
                
                stepEl.innerHTML = content;
                stepsContainer.appendChild(stepEl);
            });
        });
    }

    function formatAsMatrix(hexString) {
        // Format hex string as 4x4 matrix
        let matrix = "";
        for (let i = 0; i < Math.min(32, hexString.length); i += 2) {
            matrix += `<div class="matrix-cell">${hexString.substr(i, 2)}</div>`;
        }
        return matrix;
    }

    function animateFlowchartStages(steps) {
        const stages = document.querySelectorAll(".flow-stage");
        
        // Reset all stages
        stages.forEach(stage => {
            stage.classList.remove("active", "completed");
        });

        let currentStage = 0;
        const stageOrder = ["stage-input", "stage-key", "stage-mode", "stage-processing", "stage-output"];

        function activateNextStage() {
            if (currentStage > 0) {
                document.getElementById(stageOrder[currentStage - 1]).classList.remove("active");
                document.getElementById(stageOrder[currentStage - 1]).classList.add("completed");
            }
            
            if (currentStage < stageOrder.length) {
                document.getElementById(stageOrder[currentStage]).classList.add("active");
                currentStage++;
                
                // Animate block steps if we're in processing stage
                if (stageOrder[currentStage - 1] === "stage-processing") {
                    animateBlockSteps();
                }
                
                setTimeout(activateNextStage, 1500);
            } else {
                // Mark last stage as completed
                if (stageOrder.length > 0) {
                    document.getElementById(stageOrder[stageOrder.length - 1]).classList.remove("active");
                    document.getElementById(stageOrder[stageOrder.length - 1]).classList.add("completed");
                }
            }
        }

        // Start animation
        setTimeout(activateNextStage, 500);
    }

    function animateBlockSteps() {
        const blockSteps = document.querySelectorAll(".block-step");
        let stepIndex = 0;

        function highlightNextStep() {
            if (stepIndex < blockSteps.length) {
                // Remove previous highlight
                if (stepIndex > 0) {
                    blockSteps[stepIndex - 1].classList.remove("active");
                }
                
                // Highlight current step
                blockSteps[stepIndex].classList.add("active");
                stepIndex++;
                
                setTimeout(highlightNextStep, 800);
            }
        }

        setTimeout(highlightNextStep, 500);
    }

    function animateSteps(steps) {
        let i = 0;
        function showStep() {
            if (i >= steps.length) return;
            const step = steps[i];
            const stepEl = document.createElement("div");
            stepEl.className = "step-card";
            stepEl.innerHTML = `<strong>${step.step}</strong><pre>${step.detail}</pre>`;
            animationDiv.appendChild(stepEl);
            i++;
            setTimeout(showStep, 800);
        }
        showStep();
    }
});
