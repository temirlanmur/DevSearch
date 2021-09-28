let search_form = document.getElementById('search_form')
let page_links = document.getElementsByClassName('page-link')

if (search_form) {
    for (let i = 0; page_links.length > i; i++) {
        page_links[i].addEventListener('click', function(e) {
            e.preventDefault()

            let page = this.dataset.page
            search_form.innerHTML += `<input value=${page} name="page" hidden>`
            search_form.submit()
        })
    }
}