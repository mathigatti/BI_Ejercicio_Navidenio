# CSV2TDE Converter

multiProcessingVersion.py is a concurrent tdeConversor, it runs simultaneously multiple processes. It was deprecated due to bad  temporal performance. Parallel computation wasn't really benefitial since each process took short time to do its job and most of the time was lost waiting for shared variables that where locked to ensure good synchronization.

Testing times against the standard version (Single process) the multiProcessingVersion was twice slower than it.
