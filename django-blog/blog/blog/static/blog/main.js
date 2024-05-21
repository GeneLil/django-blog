$(document).ready(function(){
    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    $.ajaxSetup({
        beforeSend: (xhr, settings) => {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    const postsSearchInput = $("#search-posts-by-tags")
    var postSearchResultsContainer = $(".search-results")

    $(postSearchResultsContainer).addClass("display-none")

    var generateSearchResults = (posts) => {            
        $(postSearchResultsContainer).empty()
        if (posts.length == 0) {
            var emptyElement = "<li class='post-search-item'>No posts were found</li>"            
            $(postSearchResultsContainer).removeClass("display-none")
            $(postSearchResultsContainer).prepend(emptyElement)
            return
        }
        posts.forEach(post => {            
            var listElement = "<li class='post-search-item'><a href='/posts/" + post.id + "'>Title: " + post.title + "<br/> Tags:" + post.tags.join(", ") + "</a></li>"
            $(postSearchResultsContainer).removeClass("display-none")
            $(postSearchResultsContainer).prepend(listElement)
        })
    }

    var sendPostsQuery = (inputValue) => {
        $.ajax({
            type: "POST",
            url: "/get-posts-by-tags/",
            data: JSON.stringify({ tagTitle: inputValue }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: (data) => {                
                generateSearchResults(data.posts)                
            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    if (postsSearchInput.length) {
        $(postsSearchInput).on("input", function(event) { 
            $(postSearchResultsContainer).empty()
            $(postSearchResultsContainer).addClass("display-none")
            if (event.target.value.length >= 3) {
                sendPostsQuery(event.target.value) 
            }            
        } )
    }

})