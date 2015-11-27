'use strict';

/**
 * @ngdoc service
 * @name frontApp.Todo
 * @description
 * # Todo
 * Factory in the frontApp.
 */

angular.module('Ekratia').factory('Conversation', function($resource) {
  return $resource('/api/v1/conversations/:id/', {},{
        query: { method: 'GET'}
      });
});
