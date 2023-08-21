const searchForm = document.getElementById('search-form')
const folderToIndex = document.getElementById('folder-to-index')
const signature = document.getElementById('signature')
const send = document.getElementById('send')

searchForm.action = '/api/search'

send.addEventListener('click', () => {
    searchForm.action += `?folder=${folderToIndex.value}&signature=${signature.value}`
    encodeURI(searchForm.action)
})