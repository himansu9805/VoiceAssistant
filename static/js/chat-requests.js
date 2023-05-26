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

$(document).on("submit", "#prompt-form", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/chat",
    data: {
      prompt: $("#prompt").val(),
    },
    beforeSend: function () {
      $("#audio-prompt").prop("disabled", true);
      $("#send-prompt").prop("disabled", true);
      $("#prompt").prop("disabled", true);
      $("#chatgpt-response-body").html(loader);
    },
    success: function (response) {
      $("#chat-title").html(response.chat_title);
      $("#chatgpt-response-body").html(response.result);
      $("#audio-prompt").prop("disabled", false);
      $("#send-prompt").prop("disabled", false);
      $("#prompt").prop("disabled", false);
    },
  });
});
