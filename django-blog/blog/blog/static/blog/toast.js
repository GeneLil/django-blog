$.toastMarkup = (body, id) => {
    return "\
        <div class='toast-container top-0 end-0 p-3' role='alert' aria-live='assertive' aria-atomic='true'> \
            <div class='toast text-bg-primary' id='" + id + "'> \
                <div class='d-flex'> \
                    <div class='toast-body'> \
                        " + body + " \
                    </div> \
                    <button type='button' class='btn-close btn-close-white me-2 m-auto' data-bs-dismiss='toast' aria-label='Close'></button> \
                </div> \
            </div> \
        </div>"
}

$.showToast = (body, id) => {   
    const tagCreatedToast = $.toastMarkup(body, id)
    $(tagCreatedToast).appendTo("body")
 
    const toast = document.getElementById(id)
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast)
    toastBootstrap.show()        
}