$(document).ready(() => {
    const createTagButton = $("#create-tag-button")
    const tagTitleInput = $(".tags-form #title")

    const checkIfSubmitButtonEnabled = () => {        
        if ($(tagTitleInput).val().length < 3) {
            $(createTagButton).prop("disabled", true)
            return
        }
        if ($(tagTitleInput).val().length >= 3) {
            $(createTagButton).removeAttr("disabled")
        }
    }

    checkIfSubmitButtonEnabled()

    tagTitleInput.on("input", () => {              
        checkIfSubmitButtonEnabled()
    })

    const showSuccessToast = () => {        
        const toast = document.getElementById('tagCreated')
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast)
        toastBootstrap.show()        
    }

    const createTagQuery = (tagTitle) => {
        $.ajax({
            type: "POST",
            url: "/tags/new/",
            data: JSON.stringify({ tagTitle: tagTitle }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: () => {                
                showSuccessToast()                
                $(tagTitleInput).val("")
            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    $(createTagButton).on("click", () => {
        createTagQuery($(tagTitleInput).val())
    })
})