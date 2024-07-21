$(document).ready(function(){
    const postsSearchInput = $("#search-posts-by-tags")
    const postSearchResultsContainer = $(".search-results")

    $(postSearchResultsContainer).addClass("display-none")

    const generateSearchResults = (posts) => {            
        $(postSearchResultsContainer).empty()
        if (posts.length == 0) {
            const emptyElement = "<li class='post-search-item'>No posts were found</li>"            
            $(postSearchResultsContainer).removeClass("display-none")
            $(postSearchResultsContainer).prepend(emptyElement)
            return
        }
        const renderTags = (tags) => {
            tagsElement = $("<span></span>")
            tags.forEach(tag => tagsElement.append("<span class='badge text-bg-primary'>" + tag + "</span>&nbsp;"))
            return tagsElement.html()
        }
        posts.forEach(post => {            
            const listElement = "<li class='post-search-item'><a href='/posts/" + post.id + "'>Title: " + post.title + "<br/> Tags: " + renderTags(post.tags) + "</a></li>"
            $(postSearchResultsContainer).removeClass("display-none")
            $(postSearchResultsContainer).prepend(listElement)
        })
    }

    const sendPostsQuery = (inputValue) => {
        $.ajax({
            type: "POST",
            url: "/posts-by-tag/",
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