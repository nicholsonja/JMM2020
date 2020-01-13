package cs;

import java.awt.Color;
import java.awt.geom.Point2D;
import java.awt.geom.Point2D.Double;
import java.io.File;
import java.io.IOException;
import java.lang.invoke.MethodHandles;
import java.util.ArrayList;

public class Image_11 extends CSDP {
	static final int IMAGE_WIDTH_IN = 5;
	static final int IMAGE_HEIGHT_IN = 5;
	static final int DPI = 300;

	static final int NUM_THREADS = 64;
	static final int NUM_SAMPLES = 10000000;
	static final int kA = 2;
	static final int kB = 3;

	static final ArrayList<Point2D.Double> unitSegment;

	static {
		unitSegment = new ArrayList<Point2D.Double>();
		int n = 100;
		for (int i = 0; i < n; i++) {
			double t = 2 * Math.PI * i / (n - 1);
			unitSegment.add(new Point2D.Double(i / (n - 1.0), .25 * Math.sin(t)));
		}

	}

	static final Color BACKGROUND = Color.WHITE;
	static final Color FOREGROUND = new Color(0, 128, 0);

	public Image_11() {
		super(BACKGROUND, FOREGROUND);
	}

	class SegmentCalculator extends PointCalculator {

		@Override
		public Point2D.Double calculate(double k, double theta, double cx, double cy, int imageSize) {
			double radius = imageSize / 2 * .6;
			return circle(k * theta, radius, 0, 0);
		}

		@Override
		public Point2D.Double getRandomPoint(Point2D.Double a, Point2D.Double b, double cx, double cy) {
			return getRandomPoint(a, b, cx, cy, unitSegment);
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

		Image_11 imageCDSP = new Image_11();
		PointCalculator calculator = imageCDSP.new SegmentCalculator();
		imageCDSP.makeImage(height, width, imageName, NUM_THREADS, NUM_SAMPLES, kA, kB, calculator);
	}

}
