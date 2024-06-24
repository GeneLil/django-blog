$.commentMarkup = (username, avatar_url, created_at, body) => {
    return "<div class='comment-entry'>\
                <div class='comment-header'>\
                    <img src='" + avatar_url + "'>\
                    <h6>" + username + "</h6>\
                    <em class='comment-date'>" + new Date(created_at).toLocaleDateString('en-US') + "</em>\
                </div>\
                <div>" + body + "</div>\
            </div>"
}

const loadCommentsForPost = () => {
    const commentsContainer = $(".comments-container")

    const loadCommentsQuery = (postId) => {
        $.ajax({
            type: "GET",
            url: "/comments/",
            data: {
                post_id: postId,
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: ({ comments }) => {          
                drawComments(comments)
            },
            error: (error) => {
                console.log(error)
            }
        })
    } 

    const drawComments = (comments) => {
        comments.map(comment => {
            const { username, avatar_url, created_at, body } = comment
            commentElement = $.commentMarkup(username, avatar_url, created_at, body)
            $(commentsContainer).append(commentElement)
        })
    }

    const getPostId = () => window.location.pathname.split("/")[2]

    if (commentsContainer.length > 0) {  
        $(commentsContainer).empty()           
        loadCommentsQuery(getPostId())
    }
}

$(document).ready(function() {
    loadCommentsForPost()
})