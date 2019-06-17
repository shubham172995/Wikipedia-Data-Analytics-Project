public void translate() {
        Config c = Decoder.defaultConfig();
        Assets assets = null;
        File assetDir = null;
       try {
            assets = new Assets(_context);
            assetDir = assets.syncAssets();
            Log.d("DEBUG", assetDir.toString());
        } catch (IOException e) {
            Log.d("DEBUG", "Assets couldn't be created");
           e.printStackTrace();
           return;
        }

        c.setString("-hmm", new File(assetDir, "/en-us").toString());
        c.setString("-lm", new File(assetDir, "en-us.lm.dmp").toString());
        c.setString("-dict", new File(assetDir, "cmudict-en-us.dict").toString());
        Decoder d = new Decoder(c);
        FileInputStream stream = null;
        URI testwav = null;
        try {
            testwav = new URI("file:" + _wavFileName);
        } catch (URISyntaxException e) {
            e.printStackTrace();
            Log.d("DEBUG", "URI creation failed");
            return;
        }
        try {
            stream = new FileInputStream(new File(testwav));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            Log.d("DEBUG", "File stream initialization failed");
            return;
        }
        d.startUtt();
        byte[] b = new byte[4096];
        try {
            int nbytes;
            while ((nbytes = stream.read(b)) >= 0) {
                ByteBuffer bb = ByteBuffer.wrap(b, 0, nbytes);

                // Not needed on desktop but required on android
                bb.order(ByteOrder.LITTLE_ENDIAN);

                short[] s = new short[nbytes/2];
                bb.asShortBuffer().get(s);
                d.processRaw(s, nbytes/2, false, false);
            }
        } catch (IOException e) {
            e.printStackTrace();
            Log.d("DEBUG", "IO Failed");
            return;
        }
        d.endUtt();
        //System.out.println(d.hyp().getHypstr());
        //_results.add(d.hyp().getHypstr());
        SegmentList segments = d.seg();
        for (Segment seg : segments) {
            _results.add(seg.getWord());
        }
    }