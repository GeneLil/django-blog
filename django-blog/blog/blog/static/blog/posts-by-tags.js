$(document).ready(() => {
    const postsByTagsSelector = $("#postsByTagsSelector")

    if (postsByTagsSelector) {
        $(postsByTagsSelector).on("change", (event) => {                        
            window.location.href = "/posts/by-tag/" + event.currentTarget.value
        })
    }    
})