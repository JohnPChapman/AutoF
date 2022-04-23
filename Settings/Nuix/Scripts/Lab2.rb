case_factory = $utilities.getCaseFactory
begin
	caze = case_factory.create("AUTOFCASEPATH") #case is reserved so called caze
	processor = caze.createProcessor
	processor.setParallelProcessingSettings({
		"workerCount" => 4,
		"workerMemory" => 4000,
		"workerTemp" => "c:/Temp",
		"embedBroker"=> true,
		"brokerMemory" => 768
	})
	processor.setProcessingSettings({
		"processText" => true,
		"traversalScope" => "full_traversal",
		"processLooseFileContents" => true,
		"processForensicImages" => true,
		"analysisLanguage" => "en",
		"stopWords" => "none",
		"stemming" => "none",
		"enableExactQueries" => true,
		"extractNamedEntities" => true,
		"extractNamedEntitiesFromText" => true,
		"extractNamedEntitiesFromProperties" => true,
		"extractNamedEntitiesFromTextStripped" => true,
		"extractShingles" => false,
		"processTextSummaries" => true,
		"calculateSSDeepFuzzyHash" => false,
		"detectFaces" => false,
		"extractFromSlackSpace" => false,
		"carveFileSystemUnallocatedSpace" => false,
		"carveUnidentifiedData" => false,
		"carvingBlockSize" => nil,
		"recoverDeletedFiles" => true,
		"extractEndOfFileSlackSpace" => false,
		"smartProcessRegistry" => false,
		"identifyPhysicalFiles" => true,
		"createThumbnails" => true,
		#"skinToneAnalysis" => true,
		"calculateAuditedSize" => false,
		"storeBinary" => false,
		"maxStoredBinary" => 256000000,
		"maxDigestSize" => 256000000,
		"digests" => ["MD5","SHA-1"],
		"addBccToEmailDigests" => true,
		"addCommunicationDateToEmailDigests" => true,
		"reuseEvidenceStores" => true,
		"processFamilyFields" => true,
		"hideEmbeddedImmaterialData" => true,
		"reportProcessingStatus" => "physical_files"
	})
	evidence = processor.newEvidenceContainer("CASENAME", {
		"description" => "CASENAME",
		"timeZone" => "US/Pacific", #does not change case data date
		"customMetadata" => {
			"Parameter 1" => "Value 1",
			"Parameter 2" => "Value 2"
		}
	})
	evidence.addFile("AUTOFIMAGE")
	evidence.save #important
	processor.whenItemProcessed do | item |
		path = item.getPath.join("\\")
		puts "Processed #{path}"
	end
	processor.whenProgressUpdated do | info |
		puts "Progress: #{info.getCurrentSize}/#{info.getTotalSize}"
	end

	processor.whenCleaningUp do
		puts "Cleaning up..."
	end
	puts "Initiating processing"
	start = Time.now
	processor.process #starts the process
	finish = Time.now
	volume = caze.getStatistics.getFileSize("*",nil) / 1024 / 1024
	puts "Processed #{volume}MB in #{Time.at(finish - start).gmtime.strftime("%H:%M:%S")}"
rescue Exception => exc
	puts exc.message
	puts exc.backtrace.join("\n")
ensure
	if !caze.nil?
		caze.close
	end
end
