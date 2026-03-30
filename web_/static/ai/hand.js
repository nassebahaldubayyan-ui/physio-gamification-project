import {
  PoseLandmarker,
  FilesetResolver
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest";

const video = document.getElementById("video");

// لا نحتاج كانفاس نهائياً
const canvas = document.getElementById("handCanvas");
canvas.style.display = "none"; // إخفاء الكانفاس بالكامل

let prevHandX = 0.5;
const SMOOTHING = 0.7;

function smooth(prev, curr) {
  return prev * SMOOTHING + curr * (1 - SMOOTHING);
}

async function init() {
  // تشغيل الكاميرا
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;

  const vision = await FilesetResolver.forVisionTasks(
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
  );

  // POSE فقط لحساب handX
  const pose = await PoseLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath:
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task"
    },
    runningMode: "VIDEO",
    numPoses: 1
  });

 let lastSend = 0;

async function loop() {
  const now = performance.now();
  const result = await pose.detectForVideo(video, now);

  if (result.landmarks.length > 0) {
    const lm = result.landmarks[0];
    let handX = 1 - lm[16].x;
    handX = (handX - 0.4) / (0.75 - 0.4);
    handX = Math.max(0, Math.min(1, handX));
    handX = smooth(prevHandX, handX);
    prevHandX = handX;

    // إرسال كل 50ms فقط
    if (now - lastSend > 50 && window.unityInstance) {
      window.unityInstance.SendMessage(
        "Basket",
        "MoveTo",
        handX.toString()
      );
      lastSend = now;
    }
  }

  requestAnimationFrame(loop);
}

  loop();
}

init();