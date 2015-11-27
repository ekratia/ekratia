'use strict';

/**
 * @ngdoc service
 * @name frontApp.Todo
 * @description
 * # Todo
 * Factory in the frontApp.
 */

angular.module('Ekratia').factory('Referendum', function($resource) {
  return $resource('/api/v1/referendums/:id/', {},{
        query: { method: 'GET'}
      });
});
