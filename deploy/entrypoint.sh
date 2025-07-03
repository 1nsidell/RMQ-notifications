#!/bin/sh

sleep 15

faststream run notifications.main.bootstrap:get_app --factory &
taskiq worker notifications.main.bootstrap:create_taskiq_app --worker 1