
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
        clearSelectedWordChoice();
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

        wordChoice = $(this).data('word');

        //Checking if the quote word is capitalized, if it is we want to keep the new word capitalized
        if(selectedWord.html()[0] === selectedWord.html()[0].toUpperCase()){
            selectedWord.html(wordChoice.charAt(0).toUpperCase() + wordChoice.slice(1));
        } else {
            selectedWord.html(wordChoice);
        }

        $('#vote-footer').removeClass('hidden');
        $('#vote-footer').addClass('visible');
    });
}

/*---------- AJAX ----------*/

//Saves the selected word choice to the database
function saveVote(){

    word_data = {
        lastChoice : getCookie('last_choice'),
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

                if(result !== 'Failed'){
                    setLastChoiceCookie(result);
                }
                
                $('#vote-footer').removeClass('visible');
                $('#vote-footer').addClass('hidden');
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

                $('#vote-footer').removeClass('visible');
                $('#vote-footer').addClass('hidden');
                mobileShowTopWords();
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
            $('#top-words-list').append('<div class="loader-container"><div class="loader"></div>');

            setTimeout(function(){

                $('#top-words-list').html('');
                
                if(Object.keys(result).length > 0){
                    for(var choice in result){
                        $('#top-words-list').append('<li><div class="word-choice" data-word=' + result[choice].word + '>' + result[choice].word + '<span>' + result[choice].votes + '</span></div></li>');
                    }
                } else {
                    $('#top-words-list').append('<li><div class="no-top-words">No votes received, be the first!</div></li>');
                }

                addWordChoiceClickEvent();

            }, 400);
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

    //Add a little timeout so it looks like it's thinking
    setTimeout(function(){

        $('#search-results').html(' ');

        for(i = 0; i < data.length; i++){
            $('#search-results').append('<li><div class="word-choice" data-word=' + data[i].word + '>' + data[i].word + '</div></li>')
        }
        addWordChoiceClickEvent();

    }, 1000);
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

//Setting a cookie for 1 hour that will prevent the user from voting more than once
function setLastChoiceCookie(choiceId){
    var now = new Date();
    now.setTime(now.getTime() + 1 * 3600 * 1000); //1 hour
    document.cookie = 'last_choice='+ choiceId + '; expires=' + now.toUTCString() + ';';
}

//Retrievews the specified cookie's value
function getCookie(cookieName){
    var cookieString=RegExp(cookieName+"=[^;]+").exec(document.cookie);
    return decodeURIComponent(!!cookieString ? cookieString.toString().replace(/^[^=]+./,"") : "");
}

/*---------- Mobile Only ----------*/


function mobileShowTopWords(){
    if($(document).width() < 1200){
        $('#find-your-own').css('display', 'none');
        $('#top-words').css('display', 'inline-block');
    } 
}

function mobileShowFindYourOwn(){
    if($(document).width() < 1200){
        $('#find-your-own').css('display', 'inline-block');
        $('#top-words').css('display', 'none');
    } 
}

$(document).ready(function(){

    var windowWidth = $(window).width();

    //Hide top words, show search
    $('#mobile-search-toggle').on('click', function(){
        mobileShowFindYourOwn();
    });

    //Hide search, show top words
    $('#mobile-top-word-toggle').on('click', function(){
        mobileShowTopWords();
    });

    //Sets our top word and find your own divs back to being visible when resizing out of our mobile size
    $(window).resize(function(){

        var resetWordSelector;
        
        clearTimeout(resetWordSelector);

        resetWordSelector = setTimeout(() => {
            if($(document).width() > 1200){
                $('#find-your-own').css('display', 'inline-block');
                $('#top-words').css('display', 'inline-block');
            } else if($(window).width() != windowWidth) { 
                //Window width check is necessary because Safari on iOS fires off resize events without the window actually changing sizes
                mobileShowTopWords();
            }

            windowWidth = $(window).width();

        }, 100);
    })
});

/*---------- Page Ready---------*/
//Show document when quote has been prepped
$(document).ready(function(){
    $('html').show();
});