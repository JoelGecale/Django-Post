$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});


$(document).on("click", ".js-toggle-modal", function (e) {
    e.preventDefault();
    $(".js-modal").toggleClass("hidden")
})

$(document).on("click", ".js-submit", function (e) {
    e.preventDefault();
    text = $(".js-post-text").val().trim()

    if (!text) {
        return false;
    }


    $(".js-submit").prop("disabled", true).text("Posting!")
    $.ajax({
        type: 'POST',
        url: $(".js-post-text").data("post-url"),
        data: {
            text: text
        },
        success: (dataHtml) => {
            $(".js-modal").addClass("hidden");
            $("#posts-container").prepend(dataHtml);
            $(".js-submit").prop("disabled", false).text("New Post");
            $(".js-post-text").val("")
        },

        error: (error) => {
            console.warn(error)
            $(".js-submit").prop("disabled", false).text("Error");
        }
    })
})

.on("click",".js-follow", function (e) {
    e.preventDefault();
    const action=$(this).attr("data-action")

    $.ajax({
        type: 'POST',
        url: $(this).data("url"),
        data: {
            action: action,
            username: $(this).data("username")
        },
        success: (data) => {
            console.log(data)
            $(this).prop("disabled", false).text(data.wording);
           if(action =="follow"){
                $(this).attr("data-action","unfollow")
          }
        else{
            $(this).attr("data-action","follow")
          }
        },

        error: (error) => {
            console.warn(error)
        }
    })
})

$(document).on("click", ".js-toggle-card-modal", function (e) {
    e.preventDefault();
    $(".js-card-modal").toggleClass("hidden")
})
