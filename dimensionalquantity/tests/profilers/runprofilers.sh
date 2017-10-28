#!/bin/bash
kernprof -v -l *.py && python3 -m memory_profiler *.py
