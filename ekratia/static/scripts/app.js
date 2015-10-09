'use strict';

/**
 * @ngdoc overview
 * @name Ekratia
 * @description
 * # Ekratia
 *
 * Main module of the application.
 */
var app = angular
  .module('Ekratia', [
    'ngResource',
    'monospaced.elastic',
    // 'angular-humanize',
    'nl2br'
  ]);

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.config(function($httpProvider) {
$httpProvider.defaults.xsrfCookieName = 'csrftoken';
$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
$httpProvider.defaults.withCredentials = true;
});