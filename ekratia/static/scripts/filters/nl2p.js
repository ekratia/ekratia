'use strict';

angular.module('Ekratia').filter('nl2p', function () {
    return function(text){
        text = String(text).trim();
        text = text.replace(/\n\n/g, '<p class="emptyline">&nbsp;</p>\n');

        text = '<p>' + text.replace(/[\r\n]+/g, '</p><p>') + '</p>';
        // delete blank lines
        text = text.replace(/<p>\s*?<\p>/g, '<p>&nbsp;<\p>');
        // delete erroneous paragraph enclosed tags
        text = text.replace(/<p>\s*?(<.+?>)\s*?(.+?)\s*?(<\/.+?>)\s*?<\/p>/g, '$1$2$3');

        text = '<p>' + text.replace(/\n([ \t]*\n)+/g, '</p><p>')
                         .replace('\n', '<br />') + '</p>';
        return text;
    }
});
