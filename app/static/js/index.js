const folderToIndex = document.getElementById('folder-to-index')
const signature = document.getElementById('signature')
const ignore = document.getElementById('ignore')
const max = document.getElementById('range')
const indexForm = document.getElementById('index-form')
const resultsDiv = document.getElementById('results')
const noResults = document.getElementById('no-results')
const errorMessage = document.getElementById('error')
const spinner = document.getElementById('spin')

function buildCard(functionFile, functionName, functionArgs) {
    const functionCardTemplate = document.querySelector('[data-function-card]')
    const functionCard = functionCardTemplate.content.cloneNode(true).children[0]

    const filePath = functionCard.querySelector('[data-file-path]')
    filePath.textContent = functionFile

    const name = functionCard.querySelector('[data-function-name]')
    name.textContent = functionName

    const args = functionCard.querySelector('[data-function-args]')
    args.textContent = functionArgs

    return functionCard
}

signature.addEventListener('input', () => {
    document.title = signature.value !== '' ? `PPI - ${signature.value}` : 'PPI, the Python Project Indexer'
    if (signature.value.charAt(signature.value.length - 1) === '(') {
        signature.value += ')'
    }
})

indexForm.addEventListener('submit', e => {
    e.preventDefault()
    spinner.style.display = 'flex'
    noResults.style.display = 'none'
    const apiUrl = `/search?folder=${folderToIndex.value}&signature=${signature.value}&ignore=${ignore.value}&max=${max.value}`
    while (resultsDiv.firstChild) {
        resultsDiv.removeChild(resultsDiv.lastChild)
    }
    fetch(encodeURI(apiUrl))
        .then(res => res.json())
        .then(data => { 
            for (func of data) {
                // 2 spaces for easier parsing
                const splitFunc = func.split('  ')
                const s = splitFunc[1].split('(')
                const args = s[1].split(')')[0]
                const card = buildCard(splitFunc[0], s[0], args)
                resultsDiv.appendChild(card)
            }
            spinner.style.display = 'none'
        })
        .catch(() => {
            noResults.style.display = 'flex'
            errorMessage.innerHTML = `No match found for function '${signature.value}'!`
            spinner.style.display = 'none'
        })
})