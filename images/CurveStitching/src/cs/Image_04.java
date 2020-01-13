package cs;

import java.awt.Color;
import java.awt.geom.Point2D;
import java.io.File;
import java.io.IOException;
import java.lang.invoke.MethodHandles;


public class Image_04 extends CSDP {
	static final int IMAGE_WIDTH_IN = 5;
	static final int IMAGE_HEIGHT_IN = 5;
	static final int DPI = 300;

	static final int NUM_THREADS = 64;
	static final int NUM_SAMPLES = 10000000;
	static final int kA = 3;
	static final int kB = 4;	
	
	static final Color BACKGROUND = Color.WHITE;
	static final Color FOREGROUND = Color.RED;
	
	public Image_04() {
		super(BACKGROUND, FOREGROUND);
	}

	class LemniscateCalculator extends PointCalculator {

		@Override
		public Point2D.Double calculate(double k, double theta, double cx, double cy, int imageSize) {
			double radius = imageSize * .61;
			Point2D.Double p = lemniscate(k * theta, radius);
			p = rotate(p.x, p.y, -Math.PI/4);
			return new Point2D.Double(p.x + cx, p.y + cy);
		}

	}

	public static void main(String[] args) throws IOException {
		if (args.length != 1) {
			throw new IllegalArgumentException(args.length + " arguments");
		}
		File outputDir = new File(args[0]);
		if (!outputDir.isDirectory()) {
			throw new IllegalArgumentException(outputDir + " not a directory");
		}
		System.out.println(args[0]);
		String className = MethodHandles.lookup().lookupClass().getSimpleName();
		className = className.toLowerCase();
		File imageName = new File(outputDir, className + ".png");

		int width = IMAGE_WIDTH_IN * DPI;
		int height = IMAGE_HEIGHT_IN * DPI;

		Image_04 imageCDSP = new Image_04();
		PointCalculator calculator = imageCDSP.new LemniscateCalculator();
		imageCDSP.makeImage(height, width, imageName, NUM_THREADS, NUM_SAMPLES, kA, kB, calculator);
	}

}
