$(document).ready(function(){
  console.log("i'm here");

  // var ourData;

  $.get('/typeahead-data.json', function(results)
    {

    $.typeahead({
    input: ".js-typeahead",
    order: "asc",
    source: {
        data: results
    },
    callback: {
        onInit: function (node) {
            console.log('Typeahead Initiated on ' + node.selector);
        }
    }
});

 }


    );
});







































// STATUS: Monday April 17, 5:15 PM NOT working

// Instanciate the bloodhound suggestion engine 
// var findBook = new Bloodhound(
//     {
//     datumTokenizer: function(d) 
//     {
//         console.log(d);
//         return Bloodhound.tokenizers.whitespace(d.value);
//     },
//     queryTokenizer: Bloodhound.tokenizers.whitespace,
//     prefetch: '/static/all_books2.json',
    
// });



// Initialize the bloodhound suggestions engine 
// findBook.initialize();
// console.log(findBook);

// // Instanciate the typeahead UI 
// $('.searchfield').typeahead(
//     { 
//         hint: true,
//         highlight: true,
//         minLength: 1
//     },
//     {
//         name: 'books',
//         displayKey: function(findBook) {
//             console.log ("am i here?");  
//             return findBook; 
//         },
//         source: findBook
//     }
// ); 







// WAS working for Meda/Jacqui but doesnt work with all_books.json 
// $.typeahead({
//     input: ".searchfield",
//     order: "asc",
//     name: 'books',
//     source: findBook,
//     // source: {
//     //     data: ["Eat,Pray, Love - Elizabeth Gilbert", "Love me now - Medalis Trelles",]
//     // },
//     callback: {
//         onInit: function (node) {
//             console.log('Typeahead Initiated on ' + node.selector);
//         }
//     }
// });

// });

// var findBook = new Bloodhound({
//     datumTokenizer: Bloodhound.tokenizers.whitespace,
//     queryTokenizer: Bloodhound.tokenizers.whitespace,
//     prefetch: '/static/all_books.json',
//     // remote: {
//     //      url: '/books/search/%QUERY',
//     //     wildcard: '%QUERY'
//     // },

// });

// findBook.initialize();

// $('#book-search .searchfield').typeahead(
//     { 
//         hint: true,
//         highlight: true,
//         minLength: 1
//     },
//     {
//         name: 'books',
//         // display: 'book_title',
//         source: findBook
//     }
// ); 

// $.typeahead({
//     input: ".searchfield",
//     order: "asc",
//     name: 'books',
//     // source: findBook,
//     source: {
//         data: ["Eat,Pray, Love - Elizabeth Gilbert", "Love me now - Medalis Trelles",]
//     },
//     callback: {
//         onInit: function (node) {
//             console.log('Typeahead Initiated on ' + node.selector);
//         }
//     }
// });

// // });
 



