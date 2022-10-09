const search = document.querySelector('input[type="search"]');

search.onfocus = function(){
    document.getElementById('img-input').style.display = 'none';
    document.getElementById('searching').style.left = '-12.1%';
}

search.onblur = function(){
    if(search.value == ''){
        document.getElementById('img-input').style.display = 'block';
        document.getElementById('searching').style.left = '0%';
        document.getElementById('searching').style.display = 'block';
    }
}

function myFunc() {
    document.getElementById('searching').style.display = 'none';
}

document.getElementById('searching').onclick = function(){
    search.focus();
}
document.getElementById('img-input').onclick = function(){
    search.focus();
}

document.getElementById('profile').onclick = function(){
    options.style.display = 'block';
    document.getElementById('share-nav').style.pointerEvents = 'none';
}

const options = document.getElementById('options')
const posted = document.getElementById('post')
const home_nav = document.getElementById('home-nav')
const profiled = document.getElementById('profile')
const titled = document.getElementById('title')
const help_code = document.getElementById('codeHelp')
const searched = document.getElementById('searched')
const searching = document.getElementById('searching')
const inputted = document.getElementById('img-input')
const nav_sharing = document.getElementById('share-nav')

const popContainer = () =>{
    options.style.display = 'none';
    profiled.style.pointerEvents = 'none';
    home_nav.style.pointerEvents = 'none';
    titled.style.pointerEvents = 'none';
    help_code.style.pointerEvents = 'none';
    searched.style.pointerEvents = 'none';
    searching.style.pointerEvents = 'none';
    inputted.style.pointerEvents = 'none';
    nav_sharing.style.pointerEvents = 'none';
}

document.getElementById('share-nav').onclick = function(){
    posted.style.display = 'grid';
    popContainer()
}

document.getElementById('posting-today').onclick = function(){
    posted.style.display = 'grid';
    posted.style.gridTemplateColumns = '1fr 0fr';
    posted.style.width = '100vw';
    popContainer()
}

function popOff(){
    document.getElementById('options').classList.remove('active');
    document.getElementById('share-nav').style.pointerEvents = 'auto';
}

function popOff2(){
    document.getElementById('post').style.display = 'none';
    document.getElementById('profile').style.pointerEvents = 'auto';
    document.getElementById('home-nav').style.pointerEvents = 'auto';
    document.getElementById('title').style.pointerEvents = 'auto';
    document.getElementById('searching').style.pointerEvents = 'auto';
    document.getElementById('codeHelp').style.pointerEvents = 'auto';
    document.getElementById('searched').style.pointerEvents = 'auto';
    document.getElementById('img-input').style.pointerEvents = 'auto';
    document.getElementById('share-nav').style.pointerEvents = 'auto';
}

document.addEventListener('mouseup',function(e){
    var container = document.getElementById('post');
    if(!container.contains(e.target)){
        popOff2();
        popOff();
    }
});