import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Image,
  Loader2,
  CheckCircle,
  XCircle,
  Upload,
  Wand2, // Changed from MagicWand2
  Settings,
  Zap,
  Layers,
  Crop,
  RotateCcw,
  FlipHorizontal,
  Palette
} from 'lucide-react';
import { cn } from '@/lib/utils';

// Mock API functions (replace with actual API calls)
const removeBackground = async (file: File): Promise<string> => {
  // Simulate processing time
  await new Promise(resolve => setTimeout(resolve, 2000));
  // In a real implementation, you'd send the file to a backend API
  // (e.g., using a service like remove.bg or a serverless function).
  // This mock returns a placeholder image.
  return '/mock-removed-bg.png'; // Replace with a base64 string or URL
};

const enhanceImage = async (file: File): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 1500));
    return '/mock-enhanced-image.png';
};

const convertToHD = async (file: File): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return '/mock-hd-image.png';
};

const compressImage = async (file: File): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 1200));
    return '/mock-compressed-image.png';
};

const cropImage = async (file: File, options: { x: number, y: number, width: number, height: number }): Promise<string> => {
  await new Promise(resolve => setTimeout(resolve, 800));
  return '/mock-cropped-image.png';
};

const rotateImage = async (file: File, degrees: number): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return '/mock-rotated-image.png';
};

const flipImage = async (file: File, direction: 'horizontal' | 'vertical'): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return '/mock-flipped-image.png';
};

const changeFormat = async (file: File, format: 'jpg' | 'png' | 'webp'): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 700));
    return '/mock-converted-image.png';
};

// Animation Variants
const fadeInVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.5 } },
};

const slideInVariants = {
  hidden: { x: -20, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.3, ease: 'easeInOut' } },
  exit: { x: 20, opacity: 0, transition: { duration: 0.2 } },
};

const ImageEditorApp = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [processedImageUrl, setProcessedImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isHd, setIsHd] = useState(false);
  const [originalImageDimensions, setOriginalImageDimensions] = useState<{ width: number; height: number } | null>(null);
  const [cropOptions, setCropOptions] = useState<{ x: number; y: number; width: number; height: number } | null>(null);
  const [rotation, setRotation] = useState(0);
  const [flipDirection, setFlipDirection] = useState<'horizontal' | 'vertical' | null>(null);
  const [selectedFormat, setSelectedFormat] = useState<'jpg' | 'png' | 'webp'>('jpg');

  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setImageFile(file);
        setProcessedImageUrl(null); // Clear previous results
        setError(null);
        // Get original image dimensions
        const img = new Image();
        img.onload = () => {
            setOriginalImageDimensions({ width: img.width, height: img.height });
        };
        img.src = URL.createObjectURL(file);
      } else {
        setError('Invalid file type. Please upload an image.');
        setImageFile(null);
      }
    }
  };

    // Reset state when a new image is loaded
    useEffect(() => {
        setProcessedImageUrl(null);
        setLoading(false);
        setError(null);
        setCropOptions(null);
        setRotation(0);
        setFlipDirection(null);
    }, [imageFile]);

  const handleRemoveBackground = async () => {
    if (!imageFile) return;
    setLoading(true);
    setError(null);
    try {
      const resultUrl = await removeBackground(imageFile);
      setProcessedImageUrl(resultUrl);
    } catch (err: any) {
      setError(err.message || 'Failed to remove background.');
    } finally {
      setLoading(false);
    }
  };

    const handleEnhanceImage = async () => {
        if (!imageFile) return;
        setLoading(true);
        setError(null);
        try {
            const resultUrl = await enhanceImage(imageFile);
            setProcessedImageUrl(resultUrl);
        } catch (error: any) {
            setError(error.message || 'Failed to enhance image.');
        } finally {
            setLoading(false);
        }
    };

    const handleConvertToHD = async () => {
        if (!imageFile) return;
        setLoading(true);
        setError(null);
        try {
            const resultUrl = await convertToHD(imageFile);
            setProcessedImageUrl(resultUrl);
            setIsHd(true);
        } catch (error: any) {
            setError(error.message || 'Failed to convert to HD.');
        } finally {
            setLoading(false);
        }
    };

    const handleCompressImage = async () => {
        if (!imageFile) return;
        setLoading(true);
        setError(null);
        try {
            const resultUrl = await compressImage(imageFile);
            setProcessedImageUrl(resultUrl);
        } catch (error: any) {
            setError(error.message || 'Failed to compress image.');
        } finally {
            setLoading(false);
        }
    };

    const handleCrop = async () => {
      if (!imageFile || !cropOptions) return;
      setLoading(true);
      setError(null);
      try {
        const resultUrl = await cropImage(imageFile, cropOptions);
        setProcessedImageUrl(resultUrl);
        setCropOptions(null); // Reset crop options after processing
      } catch (error: any) {
        setError(error.message || 'Failed to crop image.');
      } finally {
        setLoading(false);
      }
    };

    const handleRotate = async () => {
        if (!imageFile) return;
        setLoading(true);
        setError(null);
        try {
            const resultUrl = await rotateImage(imageFile, rotation);
            setProcessedImageUrl(resultUrl);
        } catch (error: any) {
            setError(error.message || 'Failed to rotate image');
        } finally {
            setLoading(false);
        }
    };

    const handleFlip = async () => {
        if(!imageFile || !flipDirection) return;
        setLoading(true);
        setError(null);
        try{
            const resultUrl = await flipImage(imageFile, flipDirection);
            setProcessedImageUrl(resultUrl);
        } catch(error: any){
            setError(error.message || 'Failed to flip image');
        } finally {
            setLoading(false);
        }
    }

    const handleFormatChange = async () => {
        if (!imageFile) return;
        setLoading(true);
        setError(null);
        try {
            const resultUrl = await changeFormat(imageFile, selectedFormat);
            setProcessedImageUrl(resultUrl);
        } catch (error: any) {
            setError(error.message || 'Failed to change format');
        } finally {
            setLoading(false);
        }
    };

    const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

    // Function to handle setting crop options (example - using a simple rectangle)
    const handleStartCrop = () => {
        // In a real app, you'd use a UI library (like react-image-crop)
        // to allow the user to visually select the crop area.
        // For this example, we'll just set some arbitrary values.

        // For simplicity, set crop options relative to original image dimensions
        if (originalImageDimensions) {
            const { width, height } = originalImageDimensions;
            setCropOptions({
                x: width * 0.1,  // Start at 10% of width
                y: height * 0.1, // Start at 10% of height
                width: width * 0.8, // 80% of original width
                height: height * 0.6, // 60% of original height
            });
        }
    };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      {/* Header */}
      <header className="py-4 px-6 bg-gray-800/50 backdrop-blur-md border-b border-gray-700">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Palette className="w-6 h-6 text-blue-400" />
          Pixel Photo Editor
        </h1>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col md:flex-row items-center justify-center p-4">
        {/* Upload Section */}
        <div className="w-full md:w-1/2 flex flex-col items-center justify-center gap-4 p-4">
          <AnimatePresence>
            {!imageFile && (
              <motion.div
                variants={fadeInVariants}
                initial="hidden"
                animate="visible"
                className="text-center"
              >
                <Button
                  onClick={triggerFileInput}
                  variant="outline"
                  className="bg-gray-800/80 hover:bg-gray-700/80 text-gray-200 border-gray-700
                             flex items-center gap-2 px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  <Upload className="w-6 h-6" />
                  Upload Image
                </Button>
                <p className="mt-4 text-gray-400 text-sm">
                  Supported formats: JPG, PNG, WebP
                </p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  ref={fileInputRef}
                  className="hidden"
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Image Preview */}
          {imageFile && (
            <motion.div
              variants={slideInVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="relative rounded-lg overflow-hidden border border-gray-700 shadow-xl max-w-full"
            >
              <img
                ref={imageRef}
                src={URL.createObjectURL(imageFile)}
                alt="Uploaded"
                className="w-full h-auto max-h-[400px] object-contain"
              />
            </motion.div>
          )}

          {/* Display Processed Image */}
          {processedImageUrl && (
            <motion.div
              variants={slideInVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="relative rounded-lg overflow-hidden border border-gray-700 shadow-xl max-w-full mt-4" // Added mt-4
            >
              <img
                src={processedImageUrl}
                alt="Processed"
                className="w-full h-auto max-h-[400px] object-contain"
              />
              {/* Success/Error Indicator */}
              {loading ? (
                <div className="absolute inset-0 flex items-center justify-center bg-black/50">
                  <Loader2 className="w-8 h-8 text-white animate-spin" />
                </div>
              ) : error ? (
                <div className="absolute top-2 right-2 bg-red-500/80 text-white px-3 py-1 rounded-full flex items-center gap-2">
                  <XCircle className="w-5 h-5" />
                  Error
                </div>
              ) : (
                <div className="absolute top-2 right-2 bg-green-500/80 text-white px-3 py-1 rounded-full flex items-center gap-2">
                  <CheckCircle className="w-5 h-5" />
                  Done
                </div>
              )}
            </motion.div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="w-full md:w-1/2 flex flex-col items-center justify-center gap-4 p-4">
          <AnimatePresence>
            {imageFile && (
              <motion.div
                variants={slideInVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
                className="space-y-4 w-full max-w-md"
              >
                <h2 className="text-xl font-semibold">Image Tools</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-1 lg:grid-cols-2 gap-4">
                  <Button
                    onClick={handleRemoveBackground}
                    disabled={loading}
                    className="bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 border border-blue-500/30
                               transition-colors duration-300 flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Wand2 className="w-4 h-4" />
                        Remove Background
                      </>
                    )}
                  </Button>

                  <Button
                    onClick={handleEnhanceImage}
                    disabled={loading}
                    className="bg-green-500/20 hover:bg-green-500/30 text-green-400 border border-green-500/30
                               transition-colors duration-300 flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Zap className="w-4 h-4" />
                        Enhance Image
                      </>
                    )}
                  </Button>

                  <Button
                    onClick={handleConvertToHD}
                    disabled={loading || isHd}
                    className={cn(
                        "transition-colors duration-300 flex items-center justify-center gap-2",
                        isHd
                        ? "bg-gray-700 text-gray-400 border-gray-700"
                        : "bg-purple-500/20 hover:bg-purple-500/30 text-purple-400 border border-purple-500/30"
                    )}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Settings className="w-4 h-4" />
                        Convert to HD
                      </>
                    )}
                  </Button>

                  <Button
                    onClick={handleCompressImage}
                    disabled={loading}
                    className="bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-400 border border-yellow-500/30
                               transition-colors duration-300 flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Layers className="w-4 h-4" />
                        Compress Image
                      </>
                    )}
                  </Button>

                    <Button
                        onClick={handleStartCrop}
                        disabled={loading || !imageFile}
                        className="bg-pink-500/20 hover:bg-pink-500/30 text-pink-400 border border-pink-500/30 transition-colors duration-300 flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Processing...
                            </>
                        ) : (
                            <>
                                <Crop className="w-4 h-4" />
                                Crop Image
                            </>
                        )}
                    </Button>

                    {cropOptions && (
                        <Button
                            onClick={handleCrop}
                            disabled={loading || !imageFile}
                            className="bg-orange-500/20 hover:bg-orange-500/30 text-orange-400 border border-orange-500/30 transition-colors duration-300 flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    Cropping...
                                </>
                            ) : (
                                <>
                                    <Crop className="w-4 h-4" />
                                    Apply Crop
                                </>
                            )}
                        </Button>
                    )}

                    <Button
                        onClick={() => setRotation(prev => (prev + 90) % 360)}
                        disabled={loading || !imageFile}
                        className="bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-400 border border-indigo-500/30 transition-colors duration-300 flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Processing...
                            </>
                        ) : (
                            <>
                                <RotateCcw className="w-4 h-4" />
                                Rotate 90°
                            </>
                        )}
                    </Button>

                    <Button
                        onClick={() => setFlipDirection(prev => prev === 'horizontal' ? 'vertical' : 'horizontal')}
                        disabled={loading || !imageFile}
                        className="bg-teal-500/20 hover:bg-teal-500/30 text-teal-400 border border-teal-500/30 transition-colors duration-300 flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Processing...
                            </>
                        ) : (
                            <>
                                <FlipHorizontal className="w-4 h-4" />
                                Flip
                            </>
                        )}
                    </Button>
                    <div className="flex flex-col gap-2">
                        <Label htmlFor="format" className="text-sm text-gray-300">
                            Output Format
                        </Label>
                        <select
                            id="format"
                            value={selectedFormat}
                            onChange={(e) => setSelectedFormat(e.target.value as 'jpg' | 'png' | 'webp')}
                            className="bg-gray-800 border border-gray-700 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        >
                            <option value="jpg">JPG</option>
                            <option value="png">PNG</option>
                            <option value="webp">WebP</option>
                        </select>
                        <Button
                            onClick={handleFormatChange}
                            disabled={loading || !imageFile}
                            className="bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 border border-cyan-500/30 transition-colors duration-300 flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    Converting...
                                </>
                            ) : (
                                <>
                                    <Image className="w-4 h-4" />
                                    Convert Format
                                </>
                            )}
                        </Button>
                    </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-4 px-6 bg-gray-800/50 backdrop-blur-md border-t border-gray-700 text-center text-gray-400">
        <p>&copy; {new Date().getFullYear()} Pixel Photo Editor. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default ImageEditorApp;
