'use strict';

/**
 * @ngdoc service
 * @name frontApp.Todo
 * @description
 * # Todo
 * Factory in the frontApp.
 */

angular.module('Ekratia').factory('User', function($resource) {
  return $resource('/api/v1/users/:id/', {},{
        get: { method: 'GET', params: {id: '@id'}}
      });
});