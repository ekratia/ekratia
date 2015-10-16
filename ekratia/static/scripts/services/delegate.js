'use strict';

/**
 * @ngdoc service
 * @name frontApp.Todo
 * @description
 * # Todo
 * Factory in the frontApp.
 */

angular.module('Ekratia').factory('AvailableDelegate', function($resource) {
  return $resource('/api/v1/delegates/available/', {},{
        query: { method: 'GET', isArray: true }
      });
});

angular.module('Ekratia').factory('AssignedDelegate', function($resource) {
  return $resource('/api/v1/delegates/:id/', {},{
        query: { method: 'GET', isArray: true },
        delete: { method: 'DELETE', params: {id: '@id'}},
        save: { method: 'POST' }
      });
});