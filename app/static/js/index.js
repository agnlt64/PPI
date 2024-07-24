const folderToIndex = document.getElementById('folder-to-index')
const signature = document.getElementById('signature')
const ignore = document.getElementById('ignore')
const max = document.getElementById('range')
const indexForm = document.getElementById('index-form')
const resultsDiv = document.getElementById('results')
const noResults = document.getElementById('no-results')
const errorMessage = document.getElementById('error')
const spinner = document.getElementById('spin')

const isWhitespace= str => !str.replace(/\s/g, '').length

function remove(str, ch) {
    let newStr = ''
    for (let i = 0; i < str.length; ++i) {
        if (str[i] != ch) newStr += str[i]
    }
    return newStr
}

function buildCard(functionFile, functionName, functionArgs, functionDocstring) {
    const functionCardTemplate = document.querySelector('[data-function-card]')
    const functionCard = functionCardTemplate.content.cloneNode(true).children[0]

    const filePath = functionCard.querySelector('[data-file-path]')
    filePath.textContent = functionFile

    const name = functionCard.querySelector('[data-function-name]')
    name.textContent = functionName

    const args = functionCard.querySelector('[data-function-args]')
    args.textContent = functionArgs

    const docstring = functionCard.querySelector('[data-function-docstring]')
    docstring.textContent = functionDocstring

    return functionCard
}

signature.addEventListener('input', () => {
    const prevCursorPos = signature.selectionStart
    document.title = signature.value !== '' ? `PPI - ${signature.value}` : 'PPI, the Python Project Indexer'
    const len = signature.value.length
    const lastChar = signature.value.charAt(len - 1)
    if (lastChar !== ')') {
        signature.value += ')'
        signature.selectionStart = prevCursorPos
    }
    if (signature.value.includes(')') && !signature.value.includes('(')) {
        signature.value = signature.value.replace(')', '')
    }
})

indexForm.addEventListener('submit', e => {
    e.preventDefault()
    if (!isWhitespace(signature.value)) {
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
                    let docstring = 'No docstring found!'
                    if (func.docstring) docstring = func.docstring
                    // for some reason, the string.replace('`', '') method of JS
                    // does not work here so I made my own
                    docstring = remove(docstring, '`')
                    const card = buildCard(func.filename, func.name, func.args, docstring)
                    resultsDiv.appendChild(card)
                }
                spinner.style.display = 'none'
            })
            .catch(() => {
                noResults.style.display = 'flex'
                errorMessage.innerHTML = `No match found for function '${signature.value}'!`
                spinner.style.display = 'none'
            })
    }
})