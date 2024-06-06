$(document).ready(() => {
    const tagsPage = $(".tags-container")
    const createTagButton = $("#create-tag-button")
    const tagTitleInput = $(".tags-form #title")

    const tagCreatedToast = $("\
        <div class='toast-container top-0 end-0 p-3' role='alert' aria-live='assertive' aria-atomic='true'> \
            <div class='toast' id='tagCreated'> \
                <div class='d-flex'> \
                    <div class='toast-body'> \
                        Hello, world! This is a toast message. \
                    </div> \
                    <button type='button' class='btn-close me-2 m-auto' data-bs-dismiss='toast' aria-label='Close'></button> \
                </div> \
            </div> \
        </div>")

    $(tagCreatedToast).appendTo("body")

    const badgeColors = ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]

    const getRandomColor = () => {            
        const random = Math.floor(Math.random() * badgeColors.length)        
        return badgeColors[random]
    }

    const checkIfSubmitButtonEnabled = () => {        
        if ($(tagTitleInput).val().length < 3) {
            $(createTagButton).prop("disabled", true)
            return
        }
        if ($(tagTitleInput).val().length >= 3) {
            $(createTagButton).removeAttr("disabled")
        }
    }

    tagTitleInput.on("input", () => {              
        checkIfSubmitButtonEnabled()
    })

    const showSuccessToast = () => {        
        const toast = document.getElementById('tagCreated')
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast)
        toastBootstrap.show()        
    }

    const renderAllTags = (tagsResponse) => {
        const tagsContainer = $(".tags-wrapper")
        tagsResponse.forEach(tag => {
            const tagElement = "<h5><span class='badge text-bg-"+ getRandomColor() +"'>" + tag.title + "</span></h5>"
            $(tagElement).appendTo(tagsContainer)            
        })
    }

    const clearAllTags = () => {
        const tagsContainer = $(".tags-wrapper")
        $(tagsContainer).empty()
    }

    const getAllTagsQuery = () => {
        $.ajax({
            type: "GET",
            url: "/tags/all-tags",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: (data) => {          
                renderAllTags(data.tags)                                          
            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    const createTagQuery = (tagTitle) => {
        $.ajax({
            type: "POST",
            url: "/tags/new",
            data: JSON.stringify({ tagTitle: tagTitle }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: () => {     
                clearAllTags()
                getAllTagsQuery()                           
                showSuccessToast()                
                $(tagTitleInput).val("").attr("value", '')
            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    $(createTagButton).on("click", () => {
        createTagQuery($(tagTitleInput).val())
    })

    if (tagsPage.length > 0) {
        checkIfSubmitButtonEnabled()
        getAllTagsQuery()
    }
})