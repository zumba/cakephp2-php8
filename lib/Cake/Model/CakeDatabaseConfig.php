<?php
/**
 * CakePHP(tm) : Rapid Development Framework (https://cakephp.org)
 * Copyright (c) Cake Software Foundation, Inc. (https://cakefoundation.org)
 *
 * Licensed under The MIT License
 * For full copyright and license information, please see the LICENSE.txt
 * Redistributions of files must retain the above copyright notice.
 *
 * @copyright     Copyright (c) Cake Software Foundation, Inc. (https://cakefoundation.org)
 * @link          https://cakephp.org CakePHP(tm) Project
 * @package       Cake.Model
 * @license       https://opensource.org/licenses/mit-license.php MIT License
 */

/**
 * Subclass of the application's DATABASE_CONFIG that allows dynamic properties.
 *
 * ConnectionManager::create() adds runtime connections as properties of the configuration
 * object, which PHP 8.2+ reports as deprecated on classes without this attribute.
 * This file is only loaded by ConnectionManager, after app/Config/database.php.
 *
 * @package       Cake.Model
 */
#[\AllowDynamicProperties]
class CakeDatabaseConfig extends DATABASE_CONFIG {
}
