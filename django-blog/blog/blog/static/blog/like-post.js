$(document).ready(() => {
    const postDetailsPage = $(".post-details-page")

    if (postDetailsPage.length > 0) {
        const pathName = window.location.pathname
        const postId = pathName.split("/")[2]
    }
    
})