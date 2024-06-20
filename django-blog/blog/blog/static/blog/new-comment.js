$(document).ready(function() {
    const addCommentBtn = $("#addCommentButton")
    const addCommentInput = $("#addCommentInput")
    const commentsContainer = $(".comments-container")
    

    const renderComment = (comment) => {
        const {username, avatar_url, created_at, body} = comment
        const commentElement = $.commentMarkup(username, avatar_url, created_at, body)
        $(commentsContainer).prepend(commentElement)
    }

    const newCommentQuery = (postId, body) => {
        $.ajax({
            type: "POST",
            url: "/comments/new/",
            data: { 
                post_id: postId, 
                body 
            },
            success: (comment) => {                               
                $(addCommentInput).val("").attr("value", '')
                renderComment(comment)
            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    const getPostId = () => window.location.pathname.split("/")[2]

    if (addCommentBtn.length > 0) {
        $(addCommentBtn).click(() => {            
            const commentText = $(addCommentInput).val()
            newCommentQuery(getPostId(), commentText)
        })
    }
})