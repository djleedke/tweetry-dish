
var selectedWord = null;

/*---------- Initialization ----------*/

$(document).ready(function(){

    $('.quote-word').each(function(){
        ele = $(this)
        getTopChoice(ele);
    });
});

/*---------- Key Handling ----------*/

$('#search-input').keypress(function(e) {
    if(e.which == 13){

        var input = $(this).val();
        console.log(input);
        
        fetch("https://cors-anywhere.herokuapp.com/https://api.datamuse.com/sug?s=" + input)
            .then(response => response.json())
            .then(data => populateSearchResults(data));

    }
});

/*---------- On Click Events ----------*/

$(document).ready(function(){
    
    //Clicking one of our selectable words in the quote
    $('.quote-word').on('click', function(e){
        clearSelectedQuoteWord();
        $(this).addClass('selected-quote-word');
        selectedWord = $(this)

        //Some transition animations
        $('#quote').addClass('slide-up');
        $('#word-selector').addClass('visible');

        $('#search-input').focus();

        refreshTopChoices();
    });

    $('#save-button').on('click', function(e){
        saveChoice();
    });
});

function addWordChoiceClickEvent(){
    $('.word-choice').on('click', function(e){
        clearSelectedWordChoice();
        $(this).addClass('selected-word-choice');
        selectedWord.html($(this).data('word'));
    });
}

/*---------- AJAX ----------*/

//Saves the selected word choice to the database
function saveChoice(){
    $.ajax({
        type : 'POST',
        url : '/save-choice',
        data : JSON.stringify(getSelectedWords()),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            refreshTopChoices();
        }
    });
}

//Refreshes list of the top choices for the currently selected word
function refreshTopChoices(){
    $.ajax({
        type : 'POST',
        url : '/top-choices',
        data : JSON.stringify(selectedWord.data()),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            $('#top-words-list').html('');

            for(var choice in result){
                $('#top-words-list').append('<li><div class="word-choice" data-word=' + result[choice].word + '>' + result[choice].word + '<span>' + result[choice].votes + '</span></div></li>');
            }
            addWordChoiceClickEvent();
        }
    });
}

function getTopChoice(ele){
    console.log(ele.data());
    $.ajax({
        type : 'POST',
        url : '/top-choice',
        data : JSON.stringify(ele.data()),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            if (result !== 'Failed'){
                ele.html(result['word']);
            }
        }
    });
}

/*---------- Miscellaneous Functions -----------*/

function populateSearchResults(data){

    $('#search-results').html(' ');

    for(i = 0; i < data.length; i++){
        $('#search-results').append('<li><div class="word-choice" data-word=' + data[i].word + '>' + data[i].word + '</div></li>')
    }
    addWordChoiceClickEvent();
}

function getSelectedWords(){

    var selectedWords = [];

    $('.quote-word').each(function(){
        selectedWords.push($(this).html());
    });

    return selectedWords;
}

function clearSelectedQuoteWord(){
    $('.quote-word').each(function(){
        $(this).removeClass('selected-quote-word');
    });
}

function clearSelectedWordChoice(){
    $('.word-choice').each(function(){
        $(this).removeClass('selected-word-choice');
    });
}

/*---------- Page Ready---------*/
$(document).ready(function(){
    $('html').show();
});