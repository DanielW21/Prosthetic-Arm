//Pipeline:
    // 1. 
        //1.1. Input Signal Collect Raw Data and Record (allows for reusing)
        //1.2. Either do live analysis (Must be causal!)
        //1.3. Use a file analysis (Technically not causal, but can be used for testing
    // 2. Preprocess the raw data 
    // 3. Use Analysis to define the signal action and convert to an output