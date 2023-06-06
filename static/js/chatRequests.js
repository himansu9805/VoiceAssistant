let current_prompt, current_response;
const loader = `
        <div class="py-5 flex flex-col justify-center items-center">
          <div class="animate-pulse">
            Thinking by using my artificial brain for you ❤️
          </div>
          <div class="py-5 flex flex-row justify-center items-center">
            <div class="w-8 h-8 rounded-full animate-spin border-4 border-solid border-black border-t-transparent"></div>
            &nbsp;
            <div class="text-xl font-medium">Please Wait</div>
          </div>
        </div>
`;

function beforeSend() {
  $("#response-error").html("");
  $("#prompt-form").addClass("chat-disabled");
  $("#audio-prompt").prop("disabled", true);
  $("#send-prompt").prop("disabled", true);
  $("#prompt").prop("disabled", true);
  $("#processing").html(loader);
}

function success(response) {
  $("#response-about").addClass("hidden");
  $("#youtube-card").html("");
  var parsedResponseContent = String(`<div>${response.result}</div>`);
  var $parsedResponse = $(parsedResponseContent);
  $parsedResponse.find("ul").addClass("custom-list-disc mt-4 pb-6");
  $parsedResponse.find("ol").addClass("custom-list-number mt-4 pb-6");
  $parsedResponse.find("li").addClass("pl-4");
  var updatedParsedResponse = $parsedResponse.prop("outerHTML");
  $("#response-error").html("");
  $("#processing").html("");
  const audioData = response.audio;
  const audioElement = new Audio("data:audio/wav;base64," + audioData);
  audioElement.play();
  var typed = new Typed("#response-body", {
    strings: [
      `<p class="font-bold my-2">> ${response.prompt}</p><p class="my-2">${updatedParsedResponse}</p>`,
    ],
    typeSpeed: 15,
    showCursor: false,
    onBegin: () => {
      if (current_prompt != undefined || current_response != undefined) {
        $("#response-history").append(
          `<div class="my-4">
            <p class="font-bold my-2"> ${current_prompt}</p>
            <p class="my-2">${current_response}</p>
            </div>
            <div class="max-w-3xl mx-auto px-4 my-2">
              <hr class="border-skin-line" aria-hidden="true" />
            </div>`
        );
      }
      current_prompt = response.prompt;
      current_response = response.result;
    },
    onComplete: () => {
      console.log(response);
      if (response.website) {
        console.log(response);
        window.open(response.website, "_blank");
      } else if (response.youtube) {
        console.log(response.youtube);
        let description = "";
        response.youtube.descriptionSnippet.forEach((element) => {
          description += element.text + " ";
        });

        const youtubeCard = `
        <a
        id="youtube-card"
        href="${response.youtube.link}"
        target="_blank"
        class="block hover:scale-105 transition-all ease-in-out duration-200"
      >
        <div class="relative">
        <div
          class="my-4 p-4 bg-red-100 rounded-lg overflow-hidden flex flex-row justify-center items-center"
        ><div class="h-full w-3/5">
          <img
            id="youtube-thumbnail"
            class="object-cover"
            src="https://i.ytimg.com/vi/${response.youtube.id}/maxresdefault.jpg"
            alt="Video Thumbnail"
          />
        </div>
        <div class="pl-4">
          <h3 class="text-lg font-bold">${response.youtube.title}</h3>
          <p class="text-gray-600">
            ${description}
          </p>
        </div>
      </div>
      <div class="absolute bottom-2 right-4">
          <i class="fa-brands fa-youtube text-red-500 text-3xl"></i>
        </div>
      </div></a>`;
        $("#response-body").append(youtubeCard);
        current_response += youtubeCard;
        window.open(response.youtube.link, "_blank");
      }

      $("#prompt-form").removeClass("chat-disabled");
      $("#audio-prompt").prop("disabled", false);
      $("#send-prompt").prop("disabled", false);
      $("#prompt").prop("disabled", false);
    },
  });
}

function handleError(error) {
  $("#response-error").html(
    `<div class="error-container" role="alert">${error}</div>`
  );
  $("#prompt-form").removeClass("chat-disabled");
  $("#audio-prompt").prop("disabled", false);
  $("#send-prompt").prop("disabled", false);
  $("#prompt").prop("disabled", false);
  $("#processing").html("");
}

$(document).on("submit", "#prompt-form", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/chat",
    data: {
      prompt: $("#prompt").val(),
    },
    beforeSend: function () {
      beforeSend();
    },
    success: function (response) {
      success(response);
    },
    error: function (error) {
      handleError(error.responseJSON.message);
    },
  });
});

let audioContext;
let recorder;

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const input = audioContext.createMediaStreamSource(stream);
    recorder = new Recorder(input);
    recorder.record();
  });
}

function stopRecording() {
  recorder.stop();
  recorder.exportWAV(function (blob) {
    const formData = new FormData();
    formData.append("audio", blob, "recording.mp3");

    $.ajax({
      url: "/record",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      beforeSend: function () {
        beforeSend();
      },
      success: function (response) {
        success(response);
      },
      error: function (error) {
        handleError(error.responseJSON.message);
      },
    });
  });
}
