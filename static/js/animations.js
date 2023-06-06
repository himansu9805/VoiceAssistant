window.onload = (event) => {
  var typed = new Typed("#typing1", {
    strings: ["Artificial Voice Analysis and Network Intelligence"],
    typeSpeed: 25,
  });

  document.querySelector("#avani-heading-text").classList.remove("hidden");

  anime
    .timeline({ loop: false })
    .add({
      targets: "#avani-heading-text",
      translateX: ["25%", "25%"],
      opacity: [0, 1],
      easing: "easeInOutQuad",
      duration: 1000,
    })
    .add({
      targets: "#avani-heading-text",
      translateX: ["25%", "0%"],
      easing: "easeInOutQuad",
      duration: 1000,
    });

  setTimeout(() => {
    document.querySelector("#avani-description").classList.remove("hidden");
  }, 2000);

  anime.timeline({ loop: false }).add({
    targets: "#avani-description",
    translateY: [-20, 0],
    opacity: [0, 1],
    easing: "easeInOutQuad",
    duration: 500,
    delay: 2000,
  });
};

$("#record").click(function () {
  anime.timeline({ loop: true }).add({
    targets: "#grow-animation",
    scale: [1, 1.1, 1],
    easing: "easeInOutQuad",
    duration: 800,
  });
});
