// https://codepen.io/ibaslogic/pen/zYMJZaQ

const sliderEl = document.querySelector("#range")
const sliderValue = document.querySelector(".value")
const progress = (sliderEl.value / sliderEl.max) * 100;

sliderValue.innerHTML = sliderEl.value
sliderEl.style.background = `linear-gradient(to right, #1c87c9 ${progress}%, #ccc ${progress}%)`;

sliderEl.addEventListener("input", (event) => {
    const tempSliderValue = event.target.value;
    sliderValue.textContent = tempSliderValue;

    const progress = (tempSliderValue / sliderEl.max) * 100;

    sliderEl.style.background = `linear-gradient(to right, #1c87c9 ${progress}%, #ccc ${progress}%)`;
})
