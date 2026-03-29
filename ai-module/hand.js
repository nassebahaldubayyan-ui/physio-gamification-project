import { PoseLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest";

const video = document.getElementById("camera");

async function init() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/wasm"
    );

    const pose = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task"
        },
        runningMode: "VIDEO",
        numPoses: 1
    });

    async function loop() {
        const result = pose.detectForVideo(video, performance.now());

        if (result.landmarks.length > 0) {
            const hand = result.landmarks[0][16]; // اليد

            let handX = 1 - hand.x;

            let min = 0.4;
            let max = 0.75;

            handX = (handX - min) / (max - min);
            handX = Math.max(0, Math.min(1, handX));

            // إرسال لـ Unity
            if (window.unityInstance) {
                window.unityInstance.SendMessage(
                    "Basket",
                    "SetHandX",
                    handX.toString()
                );
            }
        }

        requestAnimationFrame(loop);
    }

    loop();
}

init();