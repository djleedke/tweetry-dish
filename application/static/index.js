
var selectedWord = null;

/*---------- Initialization ----------*/


$(document).ready(function(){

    
    //Getting the top choice for each of our user-editable elements
    $('.quote-word').each(function(){
        $(this).attr('data-tweetry-id', tweetryId);
        $(this).attr('data-quote-id', quoteId);
    });

    refreshQuoteWords();

});

/*---------- Key Handling ----------*/

//Waiting for an enter key press and then getting results from datamuse
$('#search-input').keypress(function(e) {

    
    if(e.which == 13){

        var input = $(this).val();

        $('#search-results').html('');
        $('#search-results').append('<div class="loader-container"><div class="loader"></div>');
        
        fetch("https://cors-anywhere.herokuapp.com/https://api.datamuse.com/sug?s=" + input)
            .then(response => response.json())
            .then(data => populateSearchResults(data));

    }

});

/*---------- On Click Events ----------*/

$(document).ready(function(){
    
    //Clicking one of our selectable words in the quote
    $('.quote-word').on('click', function(e){
        clearSelectedQuoteWord(selectedWord);
        $(this).addClass('selected-quote-word');
        selectedWord = $(this)

        //Some transition animations to show the word selector
        $('#quote').addClass('slide-up');
        $('#quote').addClass('bottom-bordered');
        $('#word-selector').addClass('visible');

        refreshTopChoiceList();
    });

    //Saving our vote
    $('#vote-button').on('click', function(e){
        saveVote();
    });
});

//Adds click event to change the selected quote word and show the vote
//footer at the bottom of the screen
function addWordChoiceClickEvent(){
    $('.word-choice').on('click', function(e){
        clearSelectedWordChoice();
        $(this).addClass('selected-word-choice');
        selectedWord.html($(this).data('word'));
        $('#vote-footer').addClass('visible');
    });
}

/*---------- AJAX ----------*/

//Saves the selected word choice to the database
function saveVote(){

    word_data = {
        tweetryId : tweetryId,
        word : selectedWord.data('word'),
        position : selectedWord.data('position'),
        choice : selectedWord.html()
    }

    $.ajax({
        type : 'POST',
        url : '/save-vote',
        data : JSON.stringify(word_data),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            //If the user is voting for an old tweetry we check on the server and refresh the page if it is
            //Other wise we refresh the top choices
            if(result === 'Refresh'){
                location.reload();
            } else {
                refreshTopChoiceList();
                refreshQuoteWords();
            }
        }
    });
}

//Refreshes each of the quote words with the top choice for that word
function refreshQuoteWords(){

    var quoteWords = $('.quote-word').map(function(){
        return $(this).data();
    }).get();

    $.ajax({
        type : 'POST',
        url : '/refresh-quote-words',
        data : JSON.stringify(quoteWords),
        contentType: 'application/json; charset=utf-8',
        success: function(result){

            $('.quote-word').each(function(){
                //Checking the results against each quote word's id, if we have
                // a match we change the html
                for(i = 0; i < result.length; i++){
                    if($(this).data('wordId') === result[i]['wordId']){
                        $(this).html(result[i]['topChoice']);
                        $(this).addClass('top-choice')
                        break;
                    } else {
                        $(this).removeClass('top-choice')
                        $(this).html($(this).data('word'));
                    }
                }
            });
        }
    });
}

//Refreshes the list of the top choices for the currently selected word
function refreshTopChoiceList(){
    $.ajax({
        type : 'POST',
        url : '/refresh-top-choice-list',
        data : JSON.stringify(selectedWord.data()),
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            $('#top-words-list').html('');

            if(Object.keys(result).length > 0){
                for(var choice in result){
                    $('#top-words-list').append('<li><div class="word-choice" data-word=' + result[choice].word + '>' + result[choice].word + '<span>' + result[choice].votes + '</span></div></li>');
                }
            } else {
                $('#top-words-list').append('<li><div class="no-top-words">No votes received, be the first!</div></li>');
            }

            addWordChoiceClickEvent();
        }
    });
}

//Gets the top choice for the specified quote word element
function getTopChoice(ele){
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

//Populates the search result ul with the provided data
function populateSearchResults(data){
    $('#search-results').html(' ');

    for(i = 0; i < data.length; i++){
        $('#search-results').append('<li><div class="word-choice" data-word=' + data[i].word + '>' + data[i].word + '</div></li>')
    }
    addWordChoiceClickEvent();
}

//Clears the selected word quote and replaces it with the current top choice
function clearSelectedQuoteWord(ele){

    if(ele !== null){
        ele.removeClass('selected-quote-word');
        refreshQuoteWords();
    }

}

//Clears the CSS from any currently selected word choices in word-selector
function clearSelectedWordChoice(){
    $('.word-choice').each(function(){
        $(this).removeClass('selected-word-choice');
    });
}

/*---------- Page Ready---------*/
//Show document when quote has been prepped
$(document).ready(function(){
    $('html').show();
});