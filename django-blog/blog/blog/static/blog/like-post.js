$(document).ready(() => {
    const postDetailsPage = $(".post-details-page")
    const likeButton = $(".like-button")
    const likeIcon = $(".bi-heart")
    const totalLikes = $(".total-likes")
    const emptyClass = "bi-heart"
    const filledClass = "bi-heart-fill"

    const getPostId = () => window.location.pathname.split("/")[2]

    const fillIcon = () => {
        $(likeIcon).removeClass(emptyClass)
        $(likeIcon).addClass(filledClass)
    }

    const emptyIcon = () => {
        $(likeIcon).removeClass(filledClass)
        $(likeIcon).addClass(emptyClass)
    }

    const processIcon = (isLiked, total_likes) => {
        isLiked ? fillIcon() : emptyIcon()
        $(totalLikes).html(total_likes)
    }

    const checkedIfLikedQuery = (postId) => {
        $.ajax({
            type: "GET",
            url: "/like/",
            data: {
                post_id: postId,
            },
            success: ({ is_liked, total_likes }) => {                          
                processIcon(is_liked, total_likes)
            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    const processLikeQuery = (postId) => {
        $.ajax({
            type: "POST",
            url: "/like/",
            data: {
                post_id: postId
            },
            success: ({is_liked}) => {            
                const toastBody = is_liked ? "Post liked" : "Post unliked"
                const toastId = is_liked ? "postLiked" : "postUnliked"
                $.showToast(toastBody, toastId)
                checkedIfLikedQuery(getPostId())
            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    const checkIfLiked = () => {
        checkedIfLikedQuery(getPostId())
    }    

    $(likeButton).click(function() {
        processLikeQuery(getPostId())
    })

    if (postDetailsPage.length > 0) {
        checkIfLiked()
    }
})