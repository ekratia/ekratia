'use strict';

/**
 * @ngdoc service
 * @name frontApp.Todo
 * @description
 * # Todo
 * Factory in the frontApp.
 */

angular.module('Ekratia').factory('VoteComment', function($resource) {
  return $resource('/api/v1/comments/votes/:id/', {},{
        query: { method: 'GET', params: {id: '@id'}, isArray: true },
        save: { method: 'POST', params: {id: '@id'} }
      });
});
